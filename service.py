from fastapi import FastAPI, HTTPException, Request, Response
from opentelemetry import trace
from pydantic import BaseModel, Field

from observability import configure_observability, get_logger
from pipeline_domain import Sample, Window

configure_observability()
logger = get_logger(__name__)
tracer = trace.get_tracer("real-time-ai-pipeline")

app = FastAPI(title="real-time-ai-pipeline", version="1.0.0")


class SamplePayload(BaseModel):
    key: str = Field(min_length=1, max_length=128)
    value: float = Field(allow_inf_nan=False)
    timestamp: float = Field(allow_inf_nan=False)


class StreamPayload(BaseModel):
    window_s: float = Field(default=60, gt=0, le=86_400, allow_inf_nan=False)
    max_samples: int = Field(default=10_000, gt=0, le=10_000)
    value: float = Field(default=0, allow_inf_nan=False)
    timestamp: float = Field(default=0, allow_inf_nan=False)
    samples: list[SamplePayload] | None = Field(default=None, max_length=10_000)


class StreamRequest(BaseModel):
    key: str = Field(min_length=1, max_length=128)
    payload: StreamPayload = Field(default_factory=StreamPayload)


@app.get("/health/live")
def live(request: Request, response: Response) -> dict[str, str]:
    request_id = request.headers.get("x-request-id", "")
    response.headers["x-request-id"] = request_id
    response.headers["x-correlation-id"] = request.headers.get("x-correlation-id", request_id)
    response.headers["x-latency-ms"] = "0.000"
    return {"status": "ok"}


@app.get("/health/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/v1/stream")
def handle(request: StreamRequest) -> dict[str, float | int | str]:
    with tracer.start_as_current_span("realtime.stream") as span:
        span.set_attribute("realtime.key", request.key)
        try:
            raw_samples = request.payload.samples
            if raw_samples is None:
                raw_samples = [
                    SamplePayload(
                        key=request.key,
                        value=request.payload.value,
                        timestamp=request.payload.timestamp,
                    )
                ]
            window = Window(request.payload.window_s, max_samples=request.payload.max_samples)
            for raw in raw_samples:
                window.add(
                    Sample(
                        key=raw.key,
                        value=raw.value,
                        timestamp=raw.timestamp,
                    )
                )
            return {
                "key": request.key,
                "window_size": len(window),
                "window_value": window.aggregate(request.key),
            }
        except (ValueError, TypeError, OverflowError) as exc:
            logger.warning("stream_request_rejected", extra={"error": str(exc)})
            raise HTTPException(status_code=400, detail=str(exc)) from exc

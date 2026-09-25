from typing import Any

from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from pydantic import BaseModel, Field

from observability import configure_observability, get_logger
from pipeline_domain import Sample, Window

configure_observability()
logger = get_logger(__name__)
tracer = trace.get_tracer("real-time-ai-pipeline")

app = FastAPI(title="real-time-ai-pipeline", version="1.0.0")


class StreamRequest(BaseModel):
    key: str
    payload: dict[str, Any] = Field(default_factory=dict)


@app.get("/health/live")
def live() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/v1/stream")
def handle(request: StreamRequest) -> dict[str, float | int | str]:
    with tracer.start_as_current_span("realtime.stream") as span:
        span.set_attribute("realtime.key", request.key)
        try:
            window_s = float(request.payload.get("window_s", 60))
            max_samples = int(request.payload.get("max_samples", 10_000))
            raw_samples = request.payload.get("samples")
            if raw_samples is None:
                raw_samples = [
                    {
                        "key": request.key,
                        "value": request.payload.get("value", 0),
                        "timestamp": request.payload.get("timestamp", 0),
                    }
                ]
            if not isinstance(raw_samples, list):
                raise TypeError("samples must be a list")
            window = Window(window_s, max_samples=max_samples)
            for raw in raw_samples:
                if not isinstance(raw, dict):
                    raise TypeError("each sample must be an object")
                window.add(
                    Sample(
                        key=str(raw.get("key", request.key)),
                        value=float(raw.get("value", 0)),
                        timestamp=float(raw.get("timestamp", 0)),
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

import time
from fastapi import FastAPI, HTTPException, Request, Response
from opentelemetry import trace
from pydantic import BaseModel, Field
from observability import configure_observability, get_logger
from pipeline_domain import Sample, Window
from runtime_evidence import request_id_from_headers, runtime_evidence
configure_observability(); logger=get_logger(__name__); tracer=trace.get_tracer("real-time-ai-pipeline"); app=FastAPI(title="real-time-ai-pipeline",version="1.0.0")
class SamplePayload(BaseModel): key:str=Field(min_length=1,max_length=128); value:float=Field(allow_inf_nan=False); timestamp:float=Field(allow_inf_nan=False)
class StreamPayload(BaseModel): window_s:float=Field(default=60,gt=0,le=86_400,allow_inf_nan=False); max_samples:int=Field(default=10_000,gt=0,le=10_000); value:float=Field(default=0,allow_inf_nan=False); timestamp:float=Field(default=0,allow_inf_nan=False); samples:list[SamplePayload]|None=Field(default=None,max_length=10_000)
class StreamRequest(BaseModel): key:str=Field(min_length=1,max_length=128); payload:StreamPayload=Field(default_factory=StreamPayload)
@app.get("/health/live")
def live(request:Request,response:Response): response.headers["x-request-id"]=request.headers.get("x-request-id",""); return {"status":"ok"}
@app.get("/health/ready")
def ready(): return {"status":"ready"}
@app.post("/v1/stream")
def handle(request:StreamRequest,http_request:Request):
 started=time.perf_counter(); request_id=request_id_from_headers(http_request.headers)
 with tracer.start_as_current_span("realtime.stream"):
  try:
   raw=request.payload.samples or [SamplePayload(key=request.key,value=request.payload.value,timestamp=request.payload.timestamp)]; window=Window(request.payload.window_s,max_samples=request.payload.max_samples)
   for item in raw: window.add(Sample(key=item.key,value=item.value,timestamp=item.timestamp))
   return {"key":request.key,"window_size":len(window),"window_value":window.aggregate(request.key),"evidence":runtime_evidence(request_id=request_id,stage="realtime.stream",decision="ALLOW",started=started)}
  except (ValueError,TypeError,OverflowError) as exc:
   evidence=runtime_evidence(request_id=request_id,stage="realtime.stream",decision="FAIL",started=started,error=str(exc)); logger.warning("stream_request_rejected",extra={"error":str(exc)}); raise HTTPException(status_code=400,detail={"error":str(exc),"evidence":evidence}) from exc

from fastapi import FastAPI
from pydantic import BaseModel
from opentelemetry import trace
try:
 from opentelemetry.sdk.resources import Resource
 from opentelemetry.sdk.trace import TracerProvider
 from opentelemetry.sdk.trace.export import BatchSpanProcessor,ConsoleSpanExporter
 p=TracerProvider(resource=Resource.create({"service.name":"real-time-ai-pipeline"}));p.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()));trace.set_tracer_provider(p)
except Exception: pass
app=FastAPI(title="real-time-ai-pipeline",version="1.0.0");tracer=trace.get_tracer("real-time-ai-pipeline")
class Request(BaseModel): key:str; payload:dict={}
@app.get("/health/live")
def live():return {"status":"ok"}
@app.get("/health/ready")
def ready():return {"status":"ready"}
@app.post("/v1/stream")
def handle(r:Request):
 with tracer.start_as_current_span("stream") as s:s.set_attribute("request.key",r.key)
 return {"status":"accepted","key":r.key}

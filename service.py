from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from opentelemetry import trace
from pipeline_domain import *
try:
 from opentelemetry.sdk.resources import Resource
 from opentelemetry.sdk.trace import TracerProvider
 from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
 p=TracerProvider(resource=Resource.create({"service.name":"real-time-ai-pipeline"}));p.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()));trace.set_tracer_provider(p)
except Exception: pass
app=FastAPI(title="real-time-ai-pipeline",version="1.0.0");tracer=trace.get_tracer("real-time-ai-pipeline")
class Request(BaseModel): key:str; payload:dict={}
@app.get("/health/live")
def live(): return {"status":"ok"}
@app.get("/health/ready")
def ready(): return {"status":"ready"}
@app.post("/v1/stream")
def handle(r:Request):
 with tracer.start_as_current_span("real-time-ai-pipeline.domain"):
  try: w=Window(float(r.payload.get("window_s",60)));w.add(Sample(r.key,float(r.payload.get("value",0)),float(r.payload.get("timestamp",0))));return {"key":r.key,"window_value":w.aggregate(r.key)}
  except (ValueError,KeyError,RuntimeError) as e: raise HTTPException(status_code=400,detail=str(e)) from e

"""Streaming pipeline core with event-time windows and bounded state."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Record: key:str; timestamp:float; value:float
class WindowOperator:
 def __init__(self,window_s=60,max_lateness_s=5):
  if window_s<=0 or max_lateness_s<0:raise ValueError("invalid window")
  self.w,self.l=window_s,max_lateness_s;self.max_seen=float("-inf");self.buckets={}
 def add(self,r):
  if r.timestamp+self.l<self.max_seen: return False
  self.max_seen=max(self.max_seen,r.timestamp);start=r.timestamp-(r.timestamp%self.w)
  self.buckets.setdefault((r.key,start),[]).append(r.value);return True
 def emit(self,watermark):
  out={}
  for k,vals in list(self.buckets.items()):
   if k[1]+self.w<=watermark:out[k]=sum(vals)/len(vals);del self.buckets[k]
  return out

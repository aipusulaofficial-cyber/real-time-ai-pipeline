from dataclasses import dataclass
from collections import deque

@dataclass(frozen=True)
class Sample:
    key:str; value:float; timestamp:float

class Window:
    def __init__(self,size_s:float): self.size_s=size_s; self._q=deque()
    def add(self,s:Sample)->None:
        if self._q and s.timestamp<self._q[-1].timestamp: raise ValueError("out-of-order sample")
        self._q.append(s); self._evict(s.timestamp)
    def _evict(self,now): 
        while self._q and now-self._q[0].timestamp>self.size_s:self._q.popleft()
    def aggregate(self,key:str)->float:
        xs=[s.value for s in self._q if s.key==key]
        return sum(xs)/len(xs) if xs else 0.0

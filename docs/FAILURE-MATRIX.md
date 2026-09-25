# Failure matrix

| Failure | Detection | Action | Retry? | Impact |
|---|---|---|---|---|
| Invalid input | validation | reject | No | 4xx |
| Dependency timeout | timeout budget | normalize | Safe/idempotent only | bounded failure/degradation |
| Dependency error | adapter | exponential backoff | Safe/idempotent only | bounded latency |
| Repeated failure | circuit breaker | open circuit | No while open | fast failure |
| Overload | bounded executor/rate limiter | fail fast/degrade | No | 429/degraded |
| Telemetry failure | exporter error | preserve domain result | exporter-local | no domain corruption |

Slow stage -> bounded buffer/backpressure; dependency timeout -> bounded retry only when safe; sustained overload -> explicit degraded mode; never allow unbounded queues.
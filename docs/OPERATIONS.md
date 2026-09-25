# Operational runbook

Golden signals: request rate, error rate, p50/p95/p99 latency, throughput, concurrency/saturation, dependency latency/errors, retry_count, circuit state and resource saturation.

1. Confirm readiness and deployment revision.
2. Trace by request_id/correlation_id.
3. Inspect error_type and dependency metrics.
4. Inspect retry_count, queue/limit saturation and circuit state.
5. Verify degraded behavior is explicit and safe.
6. Restore dependencies and run smoke/integration checks.

Inspect per-stage latency, queue depth, backpressure, dependency errors and degraded-mode counters. Recover stages gradually after saturation clears.
# Architecture

Contracts, domain logic, and infrastructure adapters are isolated. Inputs are validated, resource use is bounded, and failure semantics are explicit.

## Production trade-offs
The foundation favors deterministic local execution and small interfaces. Production should externalize shared state, use OpenTelemetry, and enforce SLO, security, and resource policies.

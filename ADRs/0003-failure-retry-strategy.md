# ADR-0003: Failure and retry strategy

## Decision
Timeouts are explicit. Retries use bounded exponential backoff and are enabled only for safe/idempotent operations. Concurrency and rate are bounded; repeated dependency failures open a circuit.

## Why
Unbounded retries amplify incidents and can duplicate side effects.

## Alternatives considered
Unlimited retries, fixed-delay retry storms, and blind retries were rejected.

## Trade-offs
Bounded latency and predictable failure require explicit caller classification.

## Consequences
Failure behavior is testable and observable.

## Implementation evidence
resilience.py and tests/test_resilience.py.
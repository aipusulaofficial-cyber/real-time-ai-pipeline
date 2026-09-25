# ADR-0004: Security decision

## Decision
Treat external input, prompts, event payloads, configuration and provider output as untrusted. Validate at boundaries, enforce least privilege, bound resources, sanitize telemetry, and fail closed for security-sensitive decisions.

## Why
AI systems cross multiple trust boundaries.

## Alternatives considered
Trusting internal callers, logging raw payloads, and fail-open authorization were rejected.

## Trade-offs
Redaction reduces debugging detail; structured categories and correlation IDs preserve diagnosis.

## Consequences
Security behavior remains deterministic and auditable.

## Implementation evidence
Service validation, structured logging, deployment hardening and security/SBOM workflows.

Security focus: Validate frame/message size and stage configuration, isolate tenant data, and redact payloads from telemetry.
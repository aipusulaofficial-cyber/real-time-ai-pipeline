# ADR-0002: Production hardening
FastAPI is the edge contract; OpenTelemetry traces requests; Kubernetes owns probes; Helm packages the workload; Terraform owns infrastructure inputs; Trivy and CycloneDX gate security/SBOM; HTTP contracts and Hypothesis protect the boundary; Locust supplies repeatable load traffic.
Failure handling is explicit through readiness/liveness and bounded resources. Production externalizes state, secrets, telemetry and autoscaling.

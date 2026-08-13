# RooomDevFlow — Agentic Software Delivery Governance

Version: `0.3.0`

RooomDevFlow is a source-available, vendor-neutral governance core for agentic software delivery. It is an independent implementation and is not affiliated with or endorsed by GitLab.

## Baseline

GitLab Duo Agent Platform is used as one comparison baseline for agentic chat, agents, flows, catalog, MCP integration, self-hosted models, contextual awareness, sandbox execution, and security analysis. RooomDevFlow is a separate product and implementation.

## Implemented in v0.3

- Vendor-neutral Agent and Flow data models
- Risk-aware policy engine for read, write, execute, network, deploy, and privileged classes
- Approval-required policy decisions for higher-risk operations
- Per-run/per-agent budget checks
- Prompt-injection detection for untrusted text
- Credential-like data redaction
- Multi-provider model routing by profile, privacy class, price, fallback order, and budget
- Offline deterministic provider for tests and disconnected environments
- Scoped TTL memory
- Structured audit-event model
- Portable Flow DAG manifests
- FastAPI endpoints for inventory, policy checks, and security scans

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
uvicorn rooomtech_dap.api:app --host 0.0.0.0 --port 8080
```

The internal `rooomtech_dap` Python import path is retained for compatibility in the `0.3.x` line. The distribution name is `rooom-devflow` and the product name is RooomDevFlow.

## Production roadmap

1. Policy-gated workflow runner with explicit resume checkpoints
2. Kubernetes sandbox executor
3. GitHub, GitLab, Bitbucket, and Azure DevOps adapters
4. Signed MCP tool registry
5. OPA/Rego integration and multi-party approvals
6. Durable event store and workers
7. OpenTelemetry and Prometheus telemetry
8. Evaluation, canary, and regression gates
9. Web console for agents, flows, approvals, policies, and budgets

## Licensing and support

Version `0.3.0` and later use the ROOOMTECH licensing terms in `LICENSE`. A separate commercial software license agreement and paid maintenance, support, implementation, integration, upgrades, security support, SLA options, private builds, and custom development are available.

Contact: `support@rooomtech.com`

Earlier releases retain their published license terms. Third-party software retains its own licenses.

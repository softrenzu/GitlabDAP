# Rooomtech DAP

Version: `0.2.0`

Rooomtech DAP is a source-available, vendor-neutral governance core for agentic software delivery. It is an independent implementation and is not affiliated with or endorsed by GitLab.

## Baseline

The design uses GitLab Duo Agent Platform as the comparison baseline: agentic chat, foundational/custom/external agents, flows, AI Catalog, MCP integration, self-hosted models, contextual awareness, sandbox execution, and security analysis.

## Implemented in v0.2

- Vendor-neutral Agent and Flow data models.
- Risk-aware policy engine for read, write, execute, network, deploy, and privileged classes.
- Approval-required policy decisions for higher-risk operations.
- Per-run/per-agent budget checks.
- Prompt-injection detection for untrusted text.
- Credential-like data redaction.
- Multi-provider model routing interface by profile, privacy class, price, fallback order, and budget.
- Offline deterministic EchoProvider for tests and disconnected environments.
- CallbackProvider adapter for deployment-specific local or cloud model SDKs.
- Scoped TTL memory with namespace deletion.
- Structured audit-event model and in-memory audit log.
- Portable Flow DAG manifests with dependencies, retry metadata, risk labels, and approval metadata.
- FastAPI endpoints for Agent/Flow/provider inventory, policy checks, and security scans.

## Why this can go beyond a single-vendor DAP

Rooomtech DAP separates governance from the Git host and model vendor. Model choice, privacy class, budget, risk classification, approval requirements, memory lifetime, and input-security checks are explicit control-plane concepts rather than being bound to one repository platform.

v0.2 is a working governance core, not a claim of production superiority over GitLab. The production execution layer is deliberately separated from the core.

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
uvicorn rooomtech_dap.api:app --host 0.0.0.0 --port 8080
```

Main endpoints:

- `GET /healthz`
- `GET /v1/agents`
- `GET /v1/flows`
- `GET /v1/providers`
- `POST /v1/policy/check`
- `POST /v1/security/scan`

## Production roadmap

1. Policy-gated workflow runner with explicit resume checkpoints.
2. Kubernetes sandbox executor with seccomp and network-policy profiles.
3. Native GitHub, GitLab, Bitbucket, and Azure DevOps adapters.
4. Signed MCP tool registry with capability grants.
5. OPA/Rego integration and multi-party approvals.
6. PostgreSQL event store and durable workers.
7. OpenTelemetry and Prometheus telemetry.
8. Golden-task evaluation, shadow traffic, canary rollout, and regression gates.
9. Web console for Agents, Flows, approvals, policies, budgets, and evaluations.

## GitLab documentation checked on 2026-08-14

- https://docs.gitlab.com/user/duo_agent_platform/
- https://docs.gitlab.com/user/duo_agent_platform/agents/
- https://docs.gitlab.com/user/duo_agent_platform/ai_catalog/
- https://docs.gitlab.com/user/duo_agent_platform/customize/
- https://docs.gitlab.com/user/duo_agent_platform/security_threats/
- https://docs.gitlab.com/user/duo_agent_platform/environment_sandbox/

## Commercial use and support

For `0.2.0` and later, noncommercial use is available under PolyForm Noncommercial License 1.0.0. Commercial or production deployment is offered under a separate paid ROOOMTECH commercial license. Paid maintenance, technical support, implementation, integration, upgrade assistance, security support, SLA options, and custom development are available. A standard commercial software license agreement is available.

Contact: `tasuku.yoshioka@rooomtech.com`

PolyForm Noncommercial License 1.0.0: https://polyformproject.org/licenses/noncommercial/1.0.0

## License

From `0.2.0`: PolyForm Noncommercial License 1.0.0 for permitted noncommercial use, or a separate paid commercial license from ROOOMTECH. Earlier versions keep the terms published with those versions.

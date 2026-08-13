# Rooomtech DAP

Rooomtech DAP is an open-source, vendor-neutral agentic software delivery platform designed to go beyond a single DevOps vendor's AI agent layer.

This repository is an independent implementation. It is not affiliated with or endorsed by GitLab.

## Why this exists

GitLab Duo Agent Platform already provides agentic chat, foundational/custom/external agents, flows, an AI catalog, MCP integration, self-hosted models, contextual awareness, and sandboxed execution. Rooomtech DAP treats those capabilities as the baseline and adds controls that are especially useful for enterprise, regulated, air-gapped, and multi-platform environments.

## Differentiators

- **Vendor-neutral control plane**: agent workflows are not tied to one Git host, CI system, model vendor, or runtime.
- **Policy-gated autonomy**: every side effect is classified by risk. Write, deploy, delete, secret access, and network actions can require explicit approval.
- **Multi-model routing**: choose models by capability, privacy class, expected quality, latency, and cost budget; automatically fall back when a provider fails.
- **Prompt-injection firewall**: untrusted tool/repository content is taint-scanned before it can influence privileged actions.
- **Scoped memory with TTL**: task/project/organization memories are isolated, expiring, redactable, and auditable.
- **Durable DAG orchestration**: parallel steps, dependencies, retries, checkpoints, resumability, and deterministic event logs.
- **Shadow/canary execution**: evaluate a new agent/model on mirrored work before granting write access.
- **Budget governance**: per-run token/cost ceilings and provider-specific limits.
- **Air-gap first**: no mandatory SaaS control plane; OpenAI-compatible local endpoints such as vLLM/NIM/TGI can be routed without code changes.
- **MCP/tool abstraction**: capability-based tool registration with allowlists and per-agent grants.
- **Observability-ready**: structured events expose model choice, policy decisions, latency, retries, security flags, and cost metadata.
- **Portable agent manifests**: agents and flows are plain YAML/JSON and can live beside code.

## Architecture

```text
Client / CI / IDE / Webhook
          |
          v
+----------------------------+
| FastAPI control plane      |
+----------------------------+
     |       |        |
     v       v        v
 Catalog   Policy   Security
     |       |        |
     +--- Orchestrator -------+
              |
       +------+-------+
       | Model Router |
       +------+-------+
              |
    local / cloud / hybrid LLMs
```

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
uvicorn rooomtech_dap.api:app --reload
```

Run a local demo flow without any external model key:

```bash
rooomtech-dap run examples/flow.yaml --goal "Add input validation to the API"
```

The default `echo` provider is deterministic and network-free. Configure an OpenAI-compatible provider when you want real inference:

```bash
export DAP_PROVIDER_URL=http://localhost:8000/v1
export DAP_PROVIDER_API_KEY=dummy
export DAP_PROVIDER_MODEL=Qwen/Qwen3-Coder
uvicorn rooomtech_dap.api:app --host 0.0.0.0 --port 8080
```

## API

- `GET /healthz`
- `GET /v1/agents`
- `GET /v1/flows`
- `POST /v1/runs`
- `GET /v1/runs/{run_id}`
- `POST /v1/policy/check`
- `POST /v1/security/scan`

## Agent manifest

```yaml
id: developer
name: Developer Agent
capabilities: [read_code, write_code, run_tests]
model_profile: coding
max_cost_usd: 2.0
```

## Flow manifest

```yaml
id: issue_to_change
steps:
  - id: inspect
    agent: planner
    prompt: Inspect the task and produce a plan.
  - id: implement
    agent: developer
    depends_on: [inspect]
    prompt: Implement the approved plan.
    risk: write
  - id: verify
    agent: reviewer
    depends_on: [implement]
    prompt: Review the change and tests.
```

## GitLab DAP baseline used for this design

Checked against GitLab's public documentation on 2026-08-14:

- https://docs.gitlab.com/user/duo_agent_platform/
- https://docs.gitlab.com/user/duo_agent_platform/agents/
- https://docs.gitlab.com/user/duo_agent_platform/ai_catalog/
- https://docs.gitlab.com/user/duo_agent_platform/customize/
- https://docs.gitlab.com/user/duo_agent_platform/security_threats/
- https://docs.gitlab.com/user/duo_agent_platform/environment_sandbox/

The claim here is a **feature-design target**, not a benchmark claim that this early implementation has already proven superior in production.

## Roadmap

1. Kubernetes sandbox executor and seccomp/network-policy profiles.
2. Native GitHub/GitLab/Bitbucket/Azure DevOps adapters.
3. MCP client/server registry with signed tool manifests.
4. OPA/Rego policy adapter and enterprise approval workflows.
5. PostgreSQL event store and resumable workers.
6. OpenTelemetry traces and Prometheus metrics.
7. Evaluation harness with golden tasks, regression gates, and shadow traffic.
8. Web UI for runs, approvals, policy, cost, and agent catalog.

## License

Apache-2.0. See `LICENSE`.

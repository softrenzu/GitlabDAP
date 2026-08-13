from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from .catalog import Catalog
from .models import PolicyInput
from .policy import PolicyEngine
from .router import ModelRouter
from .security import scan_untrusted

app = FastAPI(title="Rooomtech DAP", version="0.1.0")
catalog = Catalog()
policy = PolicyEngine()
router = ModelRouter()

class SecurityRequest(BaseModel):
    text: str

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/v1/agents")
async def agents():
    return list(catalog.agents.values())

@app.get("/v1/flows")
async def flows():
    return list(catalog.flows.values())

@app.get("/v1/providers")
async def providers():
    return [{"name": p.name, "profiles": sorted(p.profiles), "privacy": sorted(p.privacy)} for p in router.providers]

@app.post("/v1/policy/check")
async def policy_check(item: PolicyInput):
    return policy.evaluate(item)

@app.post("/v1/security/scan")
async def security_scan(item: SecurityRequest):
    return scan_untrusted(item.text)

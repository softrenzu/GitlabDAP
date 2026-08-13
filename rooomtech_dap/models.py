from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Risk(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    NETWORK = "network"
    DEPLOY = "deploy"
    PRIVILEGED = "privileged"


class AgentDefinition(BaseModel):
    id: str
    name: str
    description: str = ""
    capabilities: set[str] = Field(default_factory=set)
    model_profile: str = "general"
    system_prompt: str = "You are a software delivery agent."
    max_cost_usd: float = 1.0
    allowed_tools: set[str] = Field(default_factory=set)


class FlowStep(BaseModel):
    id: str
    agent: str
    prompt: str
    depends_on: list[str] = Field(default_factory=list)
    risk: Risk = Risk.READ
    tools: list[str] = Field(default_factory=list)
    retries: int = Field(default=1, ge=0, le=5)
    approval: bool = False


class FlowDefinition(BaseModel):
    id: str
    description: str = ""
    steps: list[FlowStep]


class RunRequest(BaseModel):
    goal: str
    flow_id: str = "issue_to_change"
    context: dict[str, Any] = Field(default_factory=dict)
    budget_usd: float = Field(default=5.0, gt=0)
    dry_run: bool = False


class StepResult(BaseModel):
    step_id: str
    status: Literal[
        "pending", "running", "approval_required", "succeeded", "failed", "skipped"
    ]
    output: str = ""
    model: str | None = None
    provider: str | None = None
    cost_usd: float = 0.0
    security_flags: list[str] = Field(default_factory=list)
    attempts: int = 0


class RunState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    flow_id: str
    goal: str
    status: Literal["created", "running", "approval_required", "succeeded", "failed"] = "created"
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    spent_usd: float = 0.0
    budget_usd: float = 5.0
    steps: dict[str, StepResult] = Field(default_factory=dict)


class PolicyInput(BaseModel):
    agent_id: str
    risk: Risk
    capabilities: set[str] = Field(default_factory=set)
    tools: list[str] = Field(default_factory=list)
    estimated_cost_usd: float = 0.0
    remaining_budget_usd: float = 0.0


class PolicyDecision(BaseModel):
    allowed: bool
    approval_required: bool = False
    reasons: list[str] = Field(default_factory=list)


class SecurityFinding(BaseModel):
    kind: str
    severity: Literal["low", "medium", "high", "critical"]
    detail: str


class SecurityScan(BaseModel):
    safe: bool
    findings: list[SecurityFinding] = Field(default_factory=list)
    redacted_text: str = ""


class ModelRequest(BaseModel):
    profile: str = "general"
    system: str
    prompt: str
    max_cost_usd: float
    privacy: Literal["public", "internal", "confidential", "restricted"] = "internal"


class ModelResponse(BaseModel):
    text: str
    model: str
    provider: str
    latency_ms: int
    estimated_cost_usd: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class AuditEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    run_id: str
    kind: str
    at: datetime = Field(default_factory=utcnow)
    data: dict[str, Any] = Field(default_factory=dict)

from __future__ import annotations

from .models import PolicyDecision, PolicyInput, Risk

_HIGH_RISK = {Risk.DEPLOY, Risk.PRIVILEGED}
_MEDIUM_RISK = {Risk.WRITE, Risk.EXECUTE, Risk.NETWORK}


class PolicyEngine:
    """Small built-in policy engine.

    It intentionally defaults to least privilege. Replace or wrap this with
    OPA/Rego in larger deployments.
    """

    def __init__(self, forbidden_tools: set[str] | None = None) -> None:
        self.forbidden_tools = forbidden_tools or set()

    def evaluate(self, item: PolicyInput) -> PolicyDecision:
        reasons: list[str] = []

        if item.estimated_cost_usd > item.remaining_budget_usd:
            return PolicyDecision(
                allowed=False,
                reasons=["Estimated model cost exceeds the remaining run budget."],
            )

        blocked = sorted(set(item.tools) & self.forbidden_tools)
        if blocked:
            return PolicyDecision(
                allowed=False,
                reasons=[f"Tools denied by policy: {', '.join(blocked)}"],
            )

        approval = item.risk in _HIGH_RISK
        if item.risk in _MEDIUM_RISK and "autonomous_side_effects" not in item.capabilities:
            approval = True
            reasons.append("Agent lacks autonomous_side_effects capability.")

        if item.risk in _HIGH_RISK:
            reasons.append(f"{item.risk.value} actions always require human approval.")

        return PolicyDecision(allowed=True, approval_required=approval, reasons=reasons)

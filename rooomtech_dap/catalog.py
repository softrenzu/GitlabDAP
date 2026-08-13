from __future__ import annotations

from .models import AgentDefinition, FlowDefinition, FlowStep, Risk


class Catalog:
    def __init__(self) -> None:
        self.agents: dict[str, AgentDefinition] = {}
        self.flows: dict[str, FlowDefinition] = {}
        self._load_defaults()

    def _load_defaults(self) -> None:
        defaults = [
            AgentDefinition(
                id="planner",
                name="Planner",
                capabilities={"read_code"},
                model_profile="planning",
                system_prompt="Plan software changes. Do not make side effects.",
            ),
            AgentDefinition(
                id="developer",
                name="Developer",
                capabilities={"read_code", "write_code", "run_tests"},
                model_profile="coding",
                system_prompt="Implement focused software changes and preserve tests.",
            ),
            AgentDefinition(
                id="reviewer",
                name="Reviewer",
                capabilities={"read_code"},
                model_profile="review",
                system_prompt="Review changes for correctness, regressions, and maintainability.",
            ),
            AgentDefinition(
                id="security",
                name="Security Analyst",
                capabilities={"read_code", "security_analysis"},
                model_profile="security",
                system_prompt="Analyze software risk defensively and propose mitigations.",
            ),
        ]
        self.agents = {agent.id: agent for agent in defaults}

        self.flows["issue_to_change"] = FlowDefinition(
            id="issue_to_change",
            description="Plan, implement, security-check, and review a requested code change.",
            steps=[
                FlowStep(
                    id="plan",
                    agent="planner",
                    prompt="Create an implementation plan for: {goal}",
                ),
                FlowStep(
                    id="implement",
                    agent="developer",
                    depends_on=["plan"],
                    prompt="Implement the goal using this plan: {plan}",
                    risk=Risk.WRITE,
                    approval=True,
                ),
                FlowStep(
                    id="security",
                    agent="security",
                    depends_on=["implement"],
                    prompt="Security review the implementation: {implement}",
                ),
                FlowStep(
                    id="review",
                    agent="reviewer",
                    depends_on=["implement"],
                    prompt="Code review the implementation: {implement}",
                ),
            ],
        )

    def agent(self, agent_id: str) -> AgentDefinition:
        if agent_id not in self.agents:
            raise KeyError(f"Unknown agent: {agent_id}")
        return self.agents[agent_id]

    def flow(self, flow_id: str) -> FlowDefinition:
        if flow_id not in self.flows:
            raise KeyError(f"Unknown flow: {flow_id}")
        return self.flows[flow_id]

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Awaitable, Callable, Protocol

from .models import ModelRequest, ModelResponse


class Provider(Protocol):
    name: str
    profiles: set[str]
    privacy: set[str]
    price_per_million_tokens: float

    async def complete(self, request: ModelRequest) -> ModelResponse: ...


@dataclass
class EchoProvider:
    name: str = "echo"
    profiles: set[str] | None = None
    privacy: set[str] | None = None
    price_per_million_tokens: float = 0.0

    def __post_init__(self) -> None:
        self.profiles = self.profiles or {"general", "coding", "review", "security", "planning"}
        self.privacy = self.privacy or {"public", "internal", "confidential", "restricted"}

    async def complete(self, request: ModelRequest) -> ModelResponse:
        started = time.perf_counter()
        return ModelResponse(
            text=f"[echo:{request.profile}] {request.prompt}",
            model="echo-1",
            provider=self.name,
            latency_ms=int((time.perf_counter() - started) * 1000),
        )


@dataclass
class CallbackProvider:
    """Adapter for SDK-backed or local model clients supplied by the deployer."""

    name: str
    callback: Callable[[ModelRequest], Awaitable[ModelResponse]]
    profiles: set[str]
    privacy: set[str]
    price_per_million_tokens: float = 0.0

    async def complete(self, request: ModelRequest) -> ModelResponse:
        return await self.callback(request)


class ModelRouter:
    """Policy-friendly provider selection with deterministic fallback."""

    def __init__(self, providers: list[Provider] | None = None) -> None:
        self.providers: list[Provider] = providers or [EchoProvider()]

    def candidates(self, request: ModelRequest) -> list[Provider]:
        eligible = [
            provider
            for provider in self.providers
            if request.profile in provider.profiles and request.privacy in provider.privacy
        ]
        return sorted(eligible, key=lambda provider: provider.price_per_million_tokens)

    async def complete(self, request: ModelRequest) -> ModelResponse:
        errors: list[str] = []
        for provider in self.candidates(request):
            try:
                result = await provider.complete(request)
                if result.estimated_cost_usd <= request.max_cost_usd:
                    return result
                errors.append(f"{provider.name}: response exceeded budget")
            except Exception as exc:
                errors.append(f"{provider.name}: {type(exc).__name__}: {exc}")
        raise RuntimeError("No model provider succeeded: " + " | ".join(errors))

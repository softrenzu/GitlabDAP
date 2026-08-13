from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any


@dataclass
class MemoryItem:
    value: Any
    expires_at: float


class ScopedMemory:
    """TTL memory isolated by scope and namespace."""

    def __init__(self) -> None:
        self._data: dict[tuple[str, str, str], MemoryItem] = {}

    def put(self, scope: str, namespace: str, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        self._data[(scope, namespace, key)] = MemoryItem(value=value, expires_at=time.time() + ttl_seconds)

    def get(self, scope: str, namespace: str, key: str) -> Any | None:
        item = self._data.get((scope, namespace, key))
        if not item:
            return None
        if item.expires_at <= time.time():
            self._data.pop((scope, namespace, key), None)
            return None
        return item.value

    def forget_namespace(self, scope: str, namespace: str) -> int:
        keys = [k for k in self._data if k[0] == scope and k[1] == namespace]
        for key in keys:
            self._data.pop(key, None)
        return len(keys)

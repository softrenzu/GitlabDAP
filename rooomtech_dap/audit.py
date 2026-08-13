from __future__ import annotations

from collections import defaultdict

from .models import AuditEvent


class AuditLog:
    def __init__(self) -> None:
        self._events: dict[str, list[AuditEvent]] = defaultdict(list)

    def append(self, run_id: str, kind: str, **data: object) -> AuditEvent:
        event = AuditEvent(run_id=run_id, kind=kind, data=dict(data))
        self._events[run_id].append(event)
        return event

    def for_run(self, run_id: str) -> list[AuditEvent]:
        return list(self._events.get(run_id, []))

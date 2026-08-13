from __future__ import annotations

import re

from .models import SecurityFinding, SecurityScan

_INJECTION_RULES = [
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.I),
    re.compile(r"reveal\s+(the\s+)?system\s+prompt", re.I),
    re.compile(r"bypass\s+(the\s+)?(policy|guardrail|approval)", re.I),
    re.compile(r"send\s+.*(credential|token|secret).*(https?://|server)", re.I),
]

_SECRET_RULES = [
    re.compile(r"(?i)(api[_-]?key|token|password)\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{12,})"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
]


def scan_untrusted(text: str) -> SecurityScan:
    findings: list[SecurityFinding] = []
    redacted = text

    for rule in _INJECTION_RULES:
        if rule.search(text):
            findings.append(
                SecurityFinding(
                    kind="prompt_injection",
                    severity="high",
                    detail=f"Untrusted content matched injection rule: {rule.pattern}",
                )
            )

    for rule in _SECRET_RULES:
        if rule.search(redacted):
            findings.append(
                SecurityFinding(
                    kind="credential_like_data",
                    severity="critical",
                    detail="Credential-like material was redacted before model/tool propagation.",
                )
            )
            redacted = rule.sub("[REDACTED]", redacted)

    return SecurityScan(
        safe=not any(f.severity in {"high", "critical"} for f in findings),
        findings=findings,
        redacted_text=redacted,
    )

"""PII guardrails — shared with PharmaGuard."""

from __future__ import annotations

import re

PII_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b\d{16}\b"),
    re.compile(r"\b(?:ssn|social security|credit card|password)\b", re.I),
]


def local_pii_check(text: str) -> str | None:
    for pattern in PII_PATTERNS:
        if pattern.search(text):
            return "PII or sensitive credential pattern detected"
    return None

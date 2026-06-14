#!/usr/bin/env python3
"""PharmaGuard Chain — autonomous clinical agent with on-chain audit journal."""

from __future__ import annotations

import argparse
import json
import sys

from clinical_brain import recommend
from guardrails import local_pii_check
from journal_client import JournalClient


def run_agent(query: str) -> dict:
    logs: list[str] = []
    logs.append("PHARMAGUARD CHAIN — Agentic Clinical Audit")
    logs.append(f"Query: {query}")

    block = local_pii_check(query)
    if block:
        return {"blocked": True, "reason": block, "logs": logs}

    logs.append("[OK] PII guardrail passed")
    recommendation = recommend(query)
    logs.append(f"[BRAIN] {recommendation['drug']} | AWaRe {recommendation['aware']}")

    journal = JournalClient()
    onchain = journal.log_decision(query, recommendation)
    logs.append(f"[JOURNAL] mode={onchain.get('mode')} tx={onchain.get('tx_hash', 'n/a')}")

    return {
        "blocked": False,
        "recommendation": recommendation,
        "onchain": onchain,
        "logs": logs,
        "pitch": "RealClaw real-life expansion: verifiable clinical agent decisions on Mantle",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="PharmaGuard Chain clinical agent")
    parser.add_argument("query", nargs="?", default="Patient eGFR 35 UTI best antibiotic?")
    args = parser.parse_args()
    result = run_agent(args.query)
    print(json.dumps(result, indent=2))
    if result.get("blocked"):
        sys.exit(2)


if __name__ == "__main__":
    main()

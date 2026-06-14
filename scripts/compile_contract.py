#!/usr/bin/env python3
"""Compile ClinicalAuditJournal.sol → artifacts/ClinicalAuditJournal.json"""

from __future__ import annotations

import json
from pathlib import Path

from solcx import compile_standard, install_solc

ROOT = Path(__file__).resolve().parent.parent
SOL = ROOT / "contracts" / "ClinicalAuditJournal.sol"
OUT = ROOT / "artifacts" / "ClinicalAuditJournal.json"


def main() -> None:
    install_solc("0.8.20")
    src = SOL.read_text(encoding="utf-8")
    compiled = compile_standard(
        {
            "language": "Solidity",
            "sources": {SOL.name: {"content": src}},
            "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}},
        },
        solc_version="0.8.20",
    )
    c = compiled["contracts"][SOL.name]["ClinicalAuditJournal"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps({"bytecode": "0x" + c["evm"]["bytecode"]["object"], "abi": c["abi"]}, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

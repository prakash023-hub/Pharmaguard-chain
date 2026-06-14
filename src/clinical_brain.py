"""Offline clinical recommendation engine — no cloud required for demo."""

from __future__ import annotations

import re

DRUG_RULES = {
    "nitrofurantoin": {
        "aware": "ACCESS",
        "renal": "Avoid if eGFR < 30",
        "note": "First-line uncomplicated lower UTI when appropriate.",
    },
    "amoxicillin": {
        "aware": "ACCESS",
        "renal": "Dose reduce if eGFR < 30",
        "note": "Use when susceptible; check allergy.",
    },
    "ciprofloxacin": {
        "aware": "WATCH",
        "renal": "Dose adjust eGFR < 50",
        "note": "Reserve — not first-line UTI.",
    },
    "metformin": {
        "aware": "ACCESS",
        "renal": "Contraindicated eGFR < 30",
        "note": "Diabetes — renal dosing critical.",
    },
}


def extract_egfr(query: str) -> int | None:
    match = re.search(r"egfr\s*(\d+)", query, re.I)
    return int(match.group(1)) if match else None


def recommend(query: str) -> dict[str, str]:
    lower = query.lower()
    egfr = extract_egfr(query)

    if "uti" in lower or "urinary" in lower:
        drug = "nitrofurantoin"
        if egfr is not None and egfr < 30:
            return {
                "drug": "consult specialist",
                "aware": "N/A",
                "rationale": f"eGFR {egfr}: nitrofurantoin contraindicated; seek alternatives.",
            }
    elif "metformin" in lower or "diabetes" in lower:
        drug = "metformin"
        if egfr is not None and egfr < 30:
            return {
                "drug": "hold metformin",
                "aware": "ACCESS",
                "rationale": f"eGFR {egfr}: metformin contraindicated per renal guidelines.",
            }
    elif "pneumonia" in lower:
        drug = "amoxicillin"
    else:
        drug = "amoxicillin"

    rule = DRUG_RULES[drug]
    return {
        "drug": drug,
        "aware": rule["aware"],
        "rationale": f"{rule['note']} {rule['renal']}",
    }

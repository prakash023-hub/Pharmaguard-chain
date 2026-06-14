# PharmaGuard Chain

**Verifiable clinical agent audit journal — [Mantle Turing Test 2026](https://dorahacks.io/hackathon/mantleturingtesthackathon2026/detail)**

> *"RealClaw gave agents hands. PharmaGuard gives clinicians proof."*

## Winning angle — Agentic Wallets & Economy track

| Requirement | Our answer |
|---|---|
| RealClaw real-life expansion | Healthcare agent — not another trading bot |
| On-chain verifiable decisions | Every recommendation hashed + logged on Mantle |
| ERC-8004 agent identity | Register agent wallet before submit (see Mantle docs) |
| Open repo + runnable demo | `python3 src/agent.py` |

**Target prize:** Track First **$8,500** + Deployment Award **$1,000**

## One-line pitch

Autonomous antibiotic steward that logs every AWaRe clinical decision on Mantle — permanent, auditable, HIPAA-friendly hashes (no PHI on-chain).

## Quick start

```bash
cd pharmaguard-chain
pip install -r requirements.txt
python3 src/agent.py "Patient eGFR 35 with UTI — best antibiotic?"
```

### On-chain mode (for judges)

1. Deploy `contracts/ClinicalAuditJournal.sol` to Mantle Sepolia
2. Set env:
   ```bash
   export MANTLE_RPC_URL=https://rpc.sepolia.mantle.xyz
   export JOURNAL_CONTRACT_ADDRESS=0xYourDeployedAddress
   export MANTLE_PRIVATE_KEY=0xYourTestnetKey
   ```
3. Re-run agent — output includes `tx_hash`

Without env vars, decisions append to `decision_journal.jsonl` (demo mode).

## Architecture

```
Clinical query → PII guardrail → Clinical brain (AWaRe rules)
                                        ↓
                          ClinicalAuditJournal.sol (Mantle)
                          queryHash + recommendationHash + AWaRe category
```

## Submit

- **Deadline:** June 15, 2026
- **Track:** Agentic Wallets & Economy
- **URL:** https://dorahacks.io/hackathon/mantleturingtesthackathon2026

## Demo video script (3 min)

1. Problem: clinical AI recommendations are not auditable
2. Run agent with sample UTI query
3. Show Mantle explorer tx OR decision_journal.jsonl
4. Human vs AI: same query, agent faster with on-chain proof

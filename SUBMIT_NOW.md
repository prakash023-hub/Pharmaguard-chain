# Mantle Submit — Do Today (deadline Jun 15)

## Your status

| Step | Status |
|------|--------|
| Agent runs | ✅ Done |
| Local journal | ✅ `decision_journal.jsonl` |
| Contract on Mantle Sepolia | ⬜ You deploy (10 min) |
| Demo video | ⬜ Record (10 min) |
| DoraHacks BUIDL | ⬜ Submit (10 min) |

**Track:** Agentic Wallets & Economy

---

## Step 1 — Deploy contract (10 min)

### A. Get testnet MNT (free)

1. Create/import wallet in MetaMask
2. Add Mantle Sepolia: RPC `https://rpc.sepolia.mantle.xyz`, Chain ID `5003`
3. Faucet: https://faucet.testnet.mantle.xyz/

### B. Deploy

```bash
cd ~/Projects/pharmaguard-chain
pip install py-solc-x   # once, if needed: /opt/anaconda3/bin/pip install py-solc-x
export MANTLE_PRIVATE_KEY=0xYourMetaMaskPrivateKey
python3 scripts/deploy_journal.py
```

Copy the `JOURNAL_CONTRACT_ADDRESS` from output.

### C. Run on-chain agent

```bash
export MANTLE_RPC_URL=https://rpc.sepolia.mantle.xyz
export JOURNAL_CONTRACT_ADDRESS=0xPasteFromDeploy
export MANTLE_PRIVATE_KEY=0xSameKey
python3 src/agent.py "Patient eGFR 35 UTI best antibiotic?"
```

Look for `"mode": "mantle_onchain"` and `"tx_hash": "0x..."`.

---

## Step 2 — Video script (2 min, read aloud)

**[Terminal — run agent]**

> "Hi, I'm Prakash. This is **PharmaGuard Chain** for the Mantle Turing Test Hackathon."

> "Clinical AI gives antibiotic advice, but there's no audit trail. We fix that."

> "Our agent checks PII guardrails, recommends **nitrofurantoin** using **AWaRe** guidelines, then logs the decision on **Mantle Sepolia**."

**[Point at `tx_hash` or `decision_journal.jsonl`]**

> "Only hashes go on-chain — no patient names or PHI."

**[Browser — Mantlescan tx]**

> "Every decision is permanent and verifiable on Mantle. RealClaw gave agents hands — PharmaGuard gives clinicians proof."

---

## Step 3 — DoraHacks BUIDL (paste this)

**Title:** PharmaGuard Chain — Clinical Agent Audit on Mantle

**Tagline:** Verifiable antibiotic stewardship decisions on Mantle Sepolia.

**Description:**

PharmaGuard Chain is a healthcare expansion of the RealClaw agent economy — not another trading bot. An autonomous clinical agent runs AWaRe antibiotic stewardship, blocks PHI patterns, and logs immutable decision hashes to `ClinicalAuditJournal.sol` on Mantle Sepolia.

**Track:** Agentic Wallets & Economy

**GitHub:** https://github.com/prakash023-hub/pharmaguard-chain (push repo first)

**Demo video:** [YouTube link]

**Mantle explorer:** [sepolia.mantlescan.xyz tx link]

---

## If deploy fails — still submit

Show `decision_journal.jsonl` + agent JSON in video. Mention "testnet deploy in README" — better than missing deadline.

**Submit URL:** https://dorahacks.io/hackathon/mantleturingtesthackathon2026

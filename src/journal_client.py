"""Mantle on-chain decision journal — deploy ClinicalAuditJournal.sol first."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from web3 import Web3

ABI = [
    {
        "inputs": [
            {"name": "queryHash", "type": "bytes32"},
            {"name": "recommendationHash", "type": "bytes32"},
            {"name": "awareCategory", "type": "string"},
        ],
        "name": "logDecision",
        "outputs": [{"name": "decisionId", "type": "bytes32"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "decisionId", "type": "bytes32"},
            {"indexed": True, "name": "agent", "type": "address"},
            {"name": "awareCategory", "type": "string"},
            {"name": "timestamp", "type": "uint256"},
        ],
        "name": "DecisionLogged",
        "type": "event",
    },
]


def _hash_text(text: str) -> bytes:
    return Web3.keccak(text=text)


class JournalClient:
    def __init__(self) -> None:
        rpc = os.environ.get("MANTLE_RPC_URL", "https://rpc.sepolia.mantle.xyz")
        self.w3 = Web3(Web3.HTTPProvider(rpc))
        address = os.environ.get("JOURNAL_CONTRACT_ADDRESS", "")
        self.enabled = bool(address)
        self.contract = (
            self.w3.eth.contract(address=Web3.to_checksum_address(address), abi=ABI)
            if self.enabled
            else None
        )
        self.private_key = os.environ.get("MANTLE_PRIVATE_KEY", "")
        self.account = self.w3.eth.account.from_key(self.private_key) if self.private_key else None

    def log_decision(self, query: str, recommendation: dict) -> dict:
        rec_text = json.dumps(recommendation, sort_keys=True)
        payload = {
            "query_hash": _hash_text(query).hex(),
            "recommendation_hash": _hash_text(rec_text).hex(),
            "aware": recommendation.get("aware", "UNKNOWN"),
            "mode": "local_journal",
        }

        if not self.enabled or not self.account or not self.contract:
            journal_path = Path(__file__).resolve().parent.parent / "decision_journal.jsonl"
            with journal_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(payload) + "\n")
            payload["note"] = f"Off-chain journal (set MANTLE_RPC_URL + JOURNAL_CONTRACT_ADDRESS): {journal_path}"
            return payload

        tx = self.contract.functions.logDecision(
            _hash_text(query),
            _hash_text(rec_text),
            recommendation.get("aware", "UNKNOWN"),
        ).build_transaction(
            {
                "from": self.account.address,
                "nonce": self.w3.eth.get_transaction_count(self.account.address),
                "gas": 200000,
                "gasPrice": self.w3.eth.gas_price,
                "chainId": self.w3.eth.chain_id,
            }
        )
        signed = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        payload["tx_hash"] = receipt.transactionHash.hex()
        payload["mode"] = "mantle_onchain"
        return payload

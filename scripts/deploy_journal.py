#!/usr/bin/env python3
"""Deploy ClinicalAuditJournal.sol to Mantle Sepolia."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from web3 import Web3

ROOT = Path(__file__).resolve().parent.parent
ARTIFACT = ROOT / "artifacts" / "ClinicalAuditJournal.json"
RPC = os.environ.get("MANTLE_RPC_URL", "https://rpc.sepolia.mantle.xyz")
EXPLORER = "https://sepolia.mantlescan.xyz"


def main() -> None:
    key = os.environ.get("MANTLE_PRIVATE_KEY", "").strip()
    if not key:
        print("Set MANTLE_PRIVATE_KEY (testnet wallet with Sepolia MNT for gas)")
        print("Faucet: https://faucet.testnet.mantle.xyz/")
        sys.exit(1)

    if not ARTIFACT.exists():
        print(f"Missing {ARTIFACT} — run: python3 scripts/compile_contract.py")
        sys.exit(1)

    artifact = json.loads(ARTIFACT.read_text())
    w3 = Web3(Web3.HTTPProvider(RPC))
    if not w3.is_connected():
        print(f"Cannot reach {RPC}")
        sys.exit(1)

    account = w3.eth.account.from_key(key)
    print(f"Deployer: {account.address}")
    print(f"Chain ID: {w3.eth.chain_id}")

    contract = w3.eth.contract(abi=artifact["abi"], bytecode=artifact["bytecode"])
    tx = contract.constructor().build_transaction(
        {
            "from": account.address,
            "nonce": w3.eth.get_transaction_count(account.address),
            "gas": 1_500_000,
            "gasPrice": w3.eth.gas_price,
            "chainId": w3.eth.chain_id,
        }
    )
    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"Deploy tx: {EXPLORER}/tx/{tx_hash.hex()}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    address = receipt.contractAddress
    if not address:
        print("Deploy failed — no contract address in receipt")
        sys.exit(1)

    print("\nSUCCESS")
    print(f"JOURNAL_CONTRACT_ADDRESS={address}")
    print(f"Explorer: {EXPLORER}/address/{address}")
    print("\nRun agent on-chain:")
    print(f"export MANTLE_RPC_URL={RPC}")
    print(f"export JOURNAL_CONTRACT_ADDRESS={address}")
    print("export MANTLE_PRIVATE_KEY=<same key>")
    print('python3 src/agent.py "Patient eGFR 35 UTI best antibiotic?"')


if __name__ == "__main__":
    main()

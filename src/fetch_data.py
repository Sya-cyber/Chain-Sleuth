# src/fetch_data.py
import requests
import os
import json
from src.config import ETHERSCAN_API_KEY, ETHERSCAN_BASE_URL

def fetch_transactions_by_address(address, output_path="data/raw/txs.json"):
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_BASE_URL, params=params)
    data = response.json()

    if data.get("status") == "1":
        with open(output_path, "w") as f:
            json.dump(data["result"], f, indent=2)
        print(f"[✓] Fetched {len(data['result'])} transactions for {address}")
    else:
        print("[✗] Failed to fetch transactions:", data.get("message"))

    return data

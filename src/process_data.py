# src/process_data.py
# src/process_data.py
import json
import pandas as pd
import os

def normalize_transactions(input_path="data/raw/txs.json", output_path="data/processed/txs.csv"):
    with open(input_path, "r") as f:
        data = json.load(f)

    if not data:
        print("[✗] No transaction data found.")
        return

    df = pd.DataFrame(data)

    # Convert types
    df["value"] = df["value"].astype(float) / 1e18  # Ether
    df["gasPrice"] = df["gasPrice"].astype(float)
    df["gasUsed"] = df["gasUsed"].astype(float)
    df["txFee_ETH"] = (df["gasUsed"] * df["gasPrice"]) / 1e18
    df["timeStamp"] = pd.to_datetime(df["timeStamp"], unit="s")

    # Clean up
    df["status"] = df["isError"].apply(lambda x: "Fail" if x == "1" else "Success")

    # Keep relevant columns
    df = df[[
        "hash", "blockNumber", "timeStamp", "from", "to", "value",
        "gasUsed", "gasPrice", "txFee_ETH", "status"
    ]]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[✓] Normalized data saved to {output_path}")


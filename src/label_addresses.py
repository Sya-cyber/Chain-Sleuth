import os
import pandas as pd

LABELS_DIR = os.path.join("data", "labels")
PROCESSED_DIR = os.path.join("data", "processed")

def load_label_dataset(filename: str) -> pd.DataFrame:
    filepath = os.path.join(LABELS_DIR, filename)

    if filename.endswith(".csv"):
        df = pd.read_csv(filepath)
    elif filename.endswith(".json"):
        df = pd.read_json(filepath)
    else:
        raise ValueError("Unsupported file type. Use .csv or .json")

    df.columns = df.columns.str.lower().str.strip()

    rename_map = {
        "address": "address",
        "entity": "label",
        "name": "label",
        "tag": "label",
        "category": "type",
        "source": "source"
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    if "address" in df.columns:
        df["address"] = df["address"].str.lower().str.strip()

    return df

def match_addresses(tx_file="txs.csv", label_file="ofac_addresses.csv", save=True):
    """
    Match blockchain addresses in transaction data with labeled OFAC addresses.

    Args:
        tx_file (str): Filename of cleaned transaction data
        label_file (str): Filename of labeled addresses (OFAC tags)
        save (bool): Whether to save the output CSV

    Returns:
        pd.DataFrame: Merged dataframe with tags
    """

    # Load datasets
    tx_path = os.path.join(PROCESSED_DIR, tx_file)
    label_path = os.path.join(LABELS_DIR, label_file)

    tx_df = pd.read_csv(tx_path)

    print("[Debug] Columns in tx_df:", tx_df.columns.tolist())

    label_df = pd.read_csv(label_path)

    # Normalize address columns
    tx_df["address"] = tx_df["to"].str.lower().str.strip()
    label_df["address"] = label_df["address"].str.lower().str.strip()

    # Merge on address
    merged = tx_df.merge(label_df, on="address", how="left")

    # Save result
    if save:
        out_path = os.path.join(PROCESSED_DIR, "txs_labeled.csv")
        merged.to_csv(out_path, index=False)
        print(f"[✔] Saved labeled transactions to {out_path}")

    return merged
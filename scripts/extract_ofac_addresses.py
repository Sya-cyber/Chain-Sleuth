import os
import xml.etree.ElementTree as ET
import pandas as pd

RAW_DIR = "data/raw"
LABELS_DIR = "data/labels"

os.makedirs(LABELS_DIR, exist_ok=True)

def extract_ofac_crypto_addresses():
    filepath = os.path.join(RAW_DIR, "sdn_advanced.xml")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"XML file not found: {filepath}")

    tree = ET.parse(filepath)
    root = tree.getroot()

    # Namespace detection
    ns_uri = root.tag.split("}")[0].strip("{")
    ns = {"ns": ns_uri}

    # Step 1: Map FeatureType IDs to crypto types
    crypto_feature_types = {}
    for ft in root.findall(".//ns:FeatureType", ns):
        ft_id = ft.attrib.get("ID")
        text = ft.text.strip() if ft.text else ""
        if text.startswith("Digital Currency Address"):
            crypto_feature_types[ft_id] = text.replace("Digital Currency Address -", "").strip()

    # Step 2: Loop through Features and extract addresses
    addresses = []
    for sdn in root.findall(".//ns:sdnEntry", ns):
        entity_name = sdn.find("ns:lastName", ns)
        entity_name = entity_name.text.strip() if entity_name is not None else "Unknown"

        for feature in sdn.findall(".//ns:Feature", ns):
            ft_id = feature.attrib.get("FeatureTypeID")
            if ft_id in crypto_feature_types:
                currency_type = crypto_feature_types[ft_id]
                value_el = feature.find("ns:FeatureValue", ns)
                if value_el is not None and value_el.text:
                    addresses.append({
                        "address": value_el.text.strip().lower(),
                        "label": "OFAC Sanctioned",
                        "type": currency_type,
                        "source": "OFAC",
                        "entity": entity_name
                    })

    # Save to CSV
    df = pd.DataFrame(addresses).drop_duplicates(subset=["address"])
    output_path = os.path.join(LABELS_DIR, "ofac_addresses.csv")
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"[✔] Extracted {len(df)} crypto addresses to {output_path}")

if __name__ == "__main__":
    extract_ofac_crypto_addresses()


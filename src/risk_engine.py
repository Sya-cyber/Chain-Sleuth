import json
import os

# Thresholds
HIGH_VOLUME_THRESHOLD = 100  # ETH or equivalent

def detect_risk_flags(address_data):
    """Check red flags in transaction data"""
    flags = {
        "uses_mixer": any(tx.get("mixer", False) for tx in address_data["transactions"]),
        "is_sanctioned": address_data.get("sanction_match", False),
        "high_volume": sum(tx["value"] for tx in address_data["transactions"]) > HIGH_VOLUME_THRESHOLD
    }
    return flags

def calculate_risk_score(flags):
    """Assign points for each red flag"""
    score = sum([
        2 if flags["is_sanctioned"] else 0,
        2 if flags["uses_mixer"] else 0,
        1 if flags["high_volume"] else 0
    ])
    
    if score >= 4:
        level = "High"
    elif score >= 2:
        level = "Medium"
    else:
        level = "Low"
    
    return {"score": score, "level": level}

def run_risk_engine(address_data):
    flags = detect_risk_flags(address_data)
    result = calculate_risk_score(flags)
    return {
        "address": address_data["address"],
        "flags": flags,
        "risk": result
    }

def generate_html_report(data, output_path="reports/risk_report_sample.html"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    html = f"""
    <html>
    <head>
        <title>Risk Report - {data['address']}</title>
        <style>
            body {{ font-family: Arial; padding: 20px; }}
            h1 {{ color: #333; }}
            .low {{ color: green; }}
            .medium {{ color: orange; }}
            .high {{ color: red; }}
        </style>
    </head>
    <body>
        <h1>Risk Report</h1>
        <p><strong>Address:</strong> {data['address']}</p>
        <p><strong>Risk Level:</strong> <span class="{data['risk']['level'].lower()}">{data['risk']['level']}</span></p>
        <p><strong>Score:</strong> {data['risk']['score']}</p>
        <h2>Flags:</h2>
        <ul>
            {"".join(f"<li><strong>{k.replace('_', ' ').title()}:</strong> {v}</li>" for k, v in data['flags'].items())}
        </ul>
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ HTML report saved to {output_path}")

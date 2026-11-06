import os

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

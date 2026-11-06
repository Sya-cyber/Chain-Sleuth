if __name__ == "__main__":
    from src import config, db_utils
    import pandas as pd

    # Load CSV to DB
    df = pd.read_csv("data/labels/ofac_addresses.csv")
    db_utils.insert_addresses(df)

    # TEST QUERYING
    conn = db_utils.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM crypto_addresses LIMIT 5;")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()

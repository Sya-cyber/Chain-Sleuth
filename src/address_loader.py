from db_connect import get_connection
from datetime import datetime

def insert_address(address, currency_type, source):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO addresses (address, currency_type, source, date_added)
        VALUES (%s, %s, %s, %s)
    """, (address, currency_type, source, datetime.now()))

    conn.commit()
    cur.close()
    conn.close()

# Example usage
if __name__ == "__main__":
    insert_address("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "BTC", "OFAC SDN list")

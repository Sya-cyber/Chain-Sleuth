from src import db_utils

conn = db_utils.get_connection()
cur = conn.cursor()
cur.execute("SELECT * FROM crypto_addresses LIMIT 5;")
rows = cur.fetchall()

print("Sample rows from DB:")
for row in rows:
    print(row)

conn.close()

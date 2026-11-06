import os
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

ETHERSCAN_BASE_URL = "https://api.etherscan.io/api"



DB_CONFIG = {
    "dbname": "chainsleuth",
    "user": "postgres",       # change if your username is different
    "password": "",  # replace with your actual password
    "host": "localhost",
    "port": 5432
}

import os
import requests
from dotenv import load_dotenv

from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)


API_KEY = os.getenv("ETHERSCAN_API_KEY")


def get_balance(address):
    url = (
        f"https://api.etherscan.io/v2/api"
        f"?chainid=1"
        f"&module=account"
        f"&action=balance"
        f"&address={address}"
        f"&tag=latest"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    if data["status"] == "1":
        wei = int(data["result"])
        eth = wei / 10**18
        return round(eth, 6)

    return 0
def get_transactions(address):
    url = (
        f"https://api.etherscan.io/v2/api"
        f"?chainid=1"
        f"&module=account"
        f"&action=txlist"
        f"&address={address}"
        f"&startblock=0"
        f"&endblock=99999999"
        f"&page=1"
        f"&offset=5"
        f"&sort=desc"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url)
    return response.json()
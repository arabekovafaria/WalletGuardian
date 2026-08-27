import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ETHERSCAN_API_KEY")


RPC_URL = "https://bsc-dataseed.bnbchain.org"


def get_balance(address):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }

    response = requests.post(RPC_URL, json=payload)
    response.raise_for_status()

    data = response.json()

    if "error" in data:
        return {"error": data["error"]}

    balance_wei = int(data["result"], 16)
    balance_bnb = balance_wei / 10**18

    return {
        "address": address,
        "balance_bnb": balance_bnb
    }
def get_transactions(address):
    url = "https://api.etherscan.io/v2/api"

    params = {
        "chainid": "56",
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": "0",
        "endblock": "99999999",
        "page": "1",
        "offset": "1",
        "sort": "desc",
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    if data.get("status") != "1" or not data.get("result"):
        return None

    tx = data["result"][0]

    return {
        "hash": tx["hash"],
        "from": tx["from"],
        "to": tx["to"],
        "value": int(tx["value"]) / 10**18,
        "timeStamp": tx["timeStamp"]
    }

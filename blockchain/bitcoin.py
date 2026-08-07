import requests


def get_transactions(address):
    url = f"https://blockstream.info/api/address/{address}/txs"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    transactions = response.json()

    if len(transactions) == 0:
        return None

    return transactions[0]
def get_balance(address):
    url = f"https://blockstream.info/api/address/{address}"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    funded = data["chain_stats"]["funded_txo_sum"]
    spent = data["chain_stats"]["spent_txo_sum"]

    balance = (funded - spent) / 100000000

    return balance
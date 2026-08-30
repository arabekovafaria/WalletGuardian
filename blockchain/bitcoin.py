import requests


def get_transactions(address):
    url = f"https://blockstream.info/api/address/{address}/txs"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    transactions = response.json()

    if len(transactions) == 0:
        return None

    tx = transactions[0]

    received = sum(
        output["value"]
        for output in tx.get("vout", [])
        if output.get("scriptpubkey_address") == address
    )

    spent = sum(
        input_data.get("prevout", {}).get("value", 0)
        for input_data in tx.get("vin", [])
        if input_data.get("prevout", {}).get("scriptpubkey_address") == address
    )

    value = (received - spent) / 100000000

    from_address = ""
    if tx.get("vin"):
        from_address = tx["vin"][0].get("prevout", {}).get(
            "scriptpubkey_address", ""
        )

    to_address = ""
    if tx.get("vout"):
        to_address = tx["vout"][0].get("scriptpubkey_address", "")

    timestamp = ""
    if tx.get("status", {}).get("confirmed"):
        timestamp = tx["status"].get("block_time", "")

    return {
        "hash": tx.get("txid", ""),
        "value": value,
        "from": from_address,
        "to": to_address,
        "timeStamp": timestamp,
    }
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
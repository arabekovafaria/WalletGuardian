from blockchain.bitcoin import get_transactions as get_btc_transactions
from blockchain.ethereum import get_transactions as get_eth_transactions

def get_transactions(chain, address):
    if chain == "eth":
        return get_eth_transactions(address)

    if chain == "btc":
        return get_btc_transactions(address)

    return None

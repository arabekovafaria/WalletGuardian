from blockchain.ethereum import get_transactions as get_eth_transactions


def get_transactions(chain, address):
    if chain == "eth":
        return get_eth_transactions(address)

    return None
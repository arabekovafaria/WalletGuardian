from blockchain.bnb import get_transactions as get_bnb_transactions
from blockchain.bitcoin import get_transactions as get_btc_transactions
from blockchain.ethereum import get_transactions as get_eth_transactions
from blockchain.solana import get_transactions as get_sol_transactions

def get_transactions(chain, address):
    if chain == "eth":
        return get_eth_transactions(address)
    
    if chain == "bnb":
        return get_bnb_transactions(address)

    if chain == "btc":
        return get_btc_transactions(address)
    
    if chain == "sol":
        return get_sol_transactions(address)

    return None

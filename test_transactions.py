from blockchain.ethereum import get_transactions

address = "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe"

tx = get_transactions(address)

print(tx)
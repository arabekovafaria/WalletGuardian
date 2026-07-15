from blockchain.transactions import get_transactions
from database.database import get_wallets

wallets = get_wallets()

if not wallets:
    print("No wallets.")
else:
    data = get_transactions(wallets[0])

    print(data)
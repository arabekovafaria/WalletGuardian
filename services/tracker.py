import asyncio
from database.database import get_wallets
from blockchain.transactions import get_transactions
from bot.bot import send_message
from datetime import datetime
last_transactions = {}

def check_wallets():
    wallets = get_wallets()


    if not wallets:
        print("No wallets found.")
        return


    for wallet_data in wallets:
        chain, wallet, chat_id = wallet_data

        latest = get_transactions(wallet)

        print("=" * 60)
        print(f"Wallet: {wallet}")

        if latest is not None:
                current_hash = latest["hash"]

                if wallet not in last_transactions:
                    last_transactions[wallet] = current_hash
                    print("First check. Transaction saved.")
                    continue
                    

                if current_hash != last_transactions[wallet]:
                    print("🚨 NEW TRANSACTION!")
                    last_transactions[wallet] = current_hash

                    

                    value = int(latest["value"]) / 10**18

                    tx_time = datetime.utcfromtimestamp(
                        int(latest["timeStamp"])
                    ).strftime("%Y-%m-%d %H:%M UTC")

                    message = (
                        f"🚨 <b>New Transaction Detected</b>\n\n"
                        f"👛 <b>Wallet</b>\n<code>{wallet}</code>\n\n"
                        f"💰 <b>Value</b>\n{value:.8f} ETH\n\n"
                        f"📤 <b>From</b>\n<code>{latest['from']}</code>\n\n"
                        f"📥 <b>To</b>\n<code>{latest['to']}</code>\n\n"
                        f"🔗 <b>Hash</b>\n<code>{latest['hash']}</code>\n\n"
                        f"🕒 <b>Time</b>\n{tx_time}"
                    )

                    asyncio.create_task(send_message(chat_id, message))
                else:
                    print("No new transaction.")
                print(f"Latest hash: {latest['hash']}")
                print(f"From: {latest['from']}")
                print(f"To: {latest['to']}")
                print(f"Value: {latest['value']}")
        else:
            print("No transactions found.")

        print("=" * 60)

async def tracker_loop():
    print("Wallet tracker started.")

    while True:
        check_wallets()
        await asyncio.sleep(30)

def start_tracker(app):
    app.create_task(tracker_loop())
    print("Wallet tracker started.")
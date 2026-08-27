import asyncio

from blockchain.transactions import get_transactions
from database.database import get_wallets

last_transactions = {}


async def check_wallets(bot):
    wallets = get_wallets()
    if not wallets:
        print("No wallets found.")
        return

    for wallet_data in wallets:
        chain, wallet, chat_id = wallet_data
        latest = get_transactions(chain, wallet)

        print("=" * 60)
        print(f"Wallet: {wallet}")

        if latest is not None:
            current_hash = latest["hash"]
            wallet_key = f"{chain}:{wallet}"

            if wallet_key not in last_transactions:
                last_transactions[wallet_key] = current_hash
                print("First check. Transaction saved.")
                continue

            if current_hash != last_transactions[wallet_key]:
                print("NEW TRANSACTION!")

                value = int(latest["value"]) / 10**18

                message = (
                    f"🚨 <b>New Transaction Detected</b>\n\n"
                    f"👛 <b>Wallet:</b>\n<code>{wallet}</code>\n\n"
                    f"💰 <b>Value:</b> {value:.8f} ETH\n\n"
                    f"📤 <b>From:</b>\n<code>{latest['from']}</code>\n\n"
                    f"📥 <b>To:</b>\n<code>{latest['to']}</code>\n\n"
                    f"🔗 <b>Hash:</b>\n<code>{latest['hash']}</code>\n\n"
                    f"🕐 <b>Time:</b>\n{latest.get('timeStamp', '')}"
                )

                await bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode="HTML",
                )

                last_transactions[wallet_key] = current_hash
            else:
                print("No new transaction.")
        else:
            print("No transactions found.")

        print("-" * 60)


async def tracker_loop(bot):
    print("Wallet tracker started.")
    while True:
        await check_wallets(bot)
        await asyncio.sleep(30)


def start_tracker_job(context):
    context.application.create_task(tracker_loop(context.bot))


def start_tracker(app):
    app.job_queue.run_once(start_tracker_job, when=0)
    print("Wallet tracker scheduled.")
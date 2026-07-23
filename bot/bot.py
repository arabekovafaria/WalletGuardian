from telegram import Update
from telegram import Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
from datetime import datetime

from database.database import (
    add_wallet,
    get_wallets,
    remove_wallet,
)
from blockchain.ethereum import get_balance, get_transactions
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

telegram_bot = Bot(token=TOKEN)

async def send_message(chat_id, text):
    await telegram_bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="HTML"
    )
app = Application.builder().token(TOKEN).build()

async def add_wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n/addwallet wallet_address"
        )
        return

    if len(context.args) != 2:
        await update.message.reply_text(
        "Usage:\n/addwallet <chain> <wallet_address>"
        )
        return

    chain = context.args[0].lower()

    wallet = context.args[1]


    chat_id = update.effective_chat.id

    add_wallet(chain, wallet, chat_id)

    await update.message.reply_text(

        f"✅ Wallet added:\n{wallet}"

    )
async def remove_wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n/removewallet wallet_address"
        )
        return

    wallet = context.args[0]

    remove_wallet(wallet)


    await update.message.reply_text(
    f"🗑 Wallet removed:\n{wallet}"
)


async def list_wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallets = get_wallets()

    if len(wallets) == 0:
        await update.message.reply_text("No wallets added.")
        return

    text = "📋 Your wallets:\n\n"

    for i, wallet in enumerate(wallets, start=1):
        chain = wallet[0]
        address = wallet[1]

        balance = get_balance(address)

        text += (
            f"{i}.\n"
            f"Chain: {chain.upper()}\n"
            f"Address:\n{address}\n\n"
            f"Balance: {balance}\n\n"
        )

    await update.message.reply_text(text)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    

    await update.message.reply_text(
        "WalletGuardian is running 🚀"
    )

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n/balance wallet_address"
        )
        return

    address = context.args[0]
    tx = get_transactions(address)
    balance = get_balance(address)

    await update.message.reply_text(
        f"💰 Wallet Balance\n\n"
        f"🌐 Network: ETH\n"
        f"📍 Address:\n{address}\n\n"
        f"💎 Balance: {balance} ETH"
    )
async def last_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n/lasttx wallet_address"
        )
        return

    address = context.args[0]

    tx = get_transactions(address)

    if tx is None:
        await update.message.reply_text("No transactions found.")
        return

    value = int(tx["value"]) / 10**18

    time = datetime.utcfromtimestamp(
        int(tx["timeStamp"])
    ).strftime("%Y-%m-%d %H:%M UTC")

    await update.message.reply_text(
        f"📦 Last Transaction\n\n"
        f"🔗 Hash\n{tx['hash']}\n\n"
        f"📤 From\n{tx['from']}\n\n"
        f"📥 To\n{tx['to']}\n\n"
        f"💰 Value\n{value} ETH\n\n"
        f"⛽ Gas Used\n{tx['gasUsed']}\n\n"
        f"🕒 Time\n{time}"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 WalletGuardian\n\n"
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/addwallet <chain> <wallet_address> - Add wallet\n"
        "/list - Show wallets\n"
        "/balance <address> - Check wallet balance\n"
        "/removewallet <address> - Remove wallet\n" 
        "/lasttx <address> - Show last transaction"  
    )
          


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("addwallet", add_wallet_command))
app.add_handler(CommandHandler("list", list_wallets))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("removewallet", remove_wallet_command))
app.add_handler(CommandHandler("lasttx", last_transaction))
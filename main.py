from bot.bot import app
from services.tracker import start_tracker


from telegram import BotCommand

async def post_init(application):
    start_tracker(application)

    await application.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Show help"),
        BotCommand("addwallet", "Add wallet"),
        BotCommand("list", "Show wallets"),
        BotCommand("balance", "Check balance"),
        BotCommand("removewallet", "Remove wallet"),
    ])
app.post_init = post_init

print("111111111111111")
app.run_polling(drop_pending_updates=True)
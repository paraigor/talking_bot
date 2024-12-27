import logging

from environs import Env
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

env = Env()
env.read_env()
TG_BOT_TOKEN = env.str("TG_BOT_TOKEN")


def start(update: Update, context: CallbackContext):
    pass


def send_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = update.message.text
    context.bot.send_message(
        text=message,
        chat_id=chat_id,
    )


def main():
    updater = Updater(TG_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, send_message)
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

import logging

from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from log_handler import TgLogHandler

logger = logging.getLogger(__file__)


def start(update: Update, context):
    update.message.reply_text("Здравствуйте!")


def echo(update: Update, context):
    text_input = dialogflow.TextInput(
        text=update.message.text, language_code="ru"
    )
    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        update.message.reply_text(response.query_result.fulfillment_text)
    except Exception as err:
        logger.info("Бот Телаграм упал с ошибкой:")
        logger.error(err)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    env = Env()
    env.read_env()
    tg_bot_token = env.str("TG_BOT_TOKEN")
    google_project_id = env.str("GOOGLE_PROJECT_ID")
    chat_id = env("TG_CHAT_ID")

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, echo)
    )

    logger.addHandler(TgLogHandler(updater.bot, chat_id))
    logger.info("Бот Телаграм запущен")

    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(
            google_project_id, tg_bot_token[21:]
        )
    except Exception as err:
        logger.info("Бот Телаграм упал с ошибкой:")
        logger.error(err)

    updater.start_polling()
    updater.idle()

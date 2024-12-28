import logging

from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Здравствуйте!")


def echo(update: Update, context: CallbackContext):
    text_input = dialogflow.TextInput(
        text=update.message.text, language_code="ru"
    )
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    update.message.reply_text(response.query_result.fulfillment_text)


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    updater = Updater(tg_bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, echo)
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    env = Env()
    env.read_env()
    tg_bot_token = env.str("TG_BOT_TOKEN")
    google_project_id = env.str("GOOGLE_PROJECT_ID")

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(google_project_id, tg_bot_token)
    main()

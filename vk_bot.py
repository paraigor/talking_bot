import logging
import random

import telegram
import vk_api
from environs import Env
from google.cloud import dialogflow
from vk_api.longpoll import VkEventType, VkLongPoll

logger = logging.getLogger(__file__)


class TgLogHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def echo(event, vk_api):
    text_input = dialogflow.TextInput(text=event.text, language_code="ru")
    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        if not response.query_result.intent.is_fallback:
            vk_api.messages.send(
                user_id=event.user_id,
                message=response.query_result.fulfillment_text,
                random_id=random.randint(1, 1000),
            )
    except Exception as err:
        logger.info("Бот упал с ошибкой:")
        logger.error(err)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    env = Env()
    env.read_env()
    vk_token = env.str("VK_GROUP_TOKEN")
    google_project_id = env.str("GOOGLE_PROJECT_ID")
    bot_token = env("TG_BOT_TOKEN")
    chat_id = env("TG_CHAT_ID")

    bot = telegram.Bot(bot_token)
    logger.addHandler(TgLogHandler(bot, chat_id))
    logger.info("Бот запущен")

    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(
            google_project_id, vk_token[9:29]
        )

        vk_session = vk_api.VkApi(token=vk_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                echo(event, vk_api)
    except Exception as err:
        logger.info("Бот упал с ошибкой:")
        logger.error(err)

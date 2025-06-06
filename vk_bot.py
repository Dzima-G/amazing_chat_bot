import logging
import os

import vk_api
from dotenv import load_dotenv
from telegram import Bot
from vk_api.exceptions import ApiError
from vk_api.longpoll import VkEventType, VkLongPoll

from dialog_flow_api import detect_intent_response
from tg_logging import TelegramLogsHandler

logger = logging.getLogger('vk_logger')


def run_vk_bot(vk_token, project_id, language_code, error_tg_token, tg_chat_id):
    if error_tg_token and tg_chat_id:
        tg_error_bot = Bot(token=error_tg_token)
        tg_error_bot.send_message(
            chat_id=tg_chat_id,
            text='Бот VK успешно запущен!'
        )

    try:
        vk_session = vk_api.VkApi(token=vk_token)
        vk = vk_session.get_api()
        logger.info('Бот VK успешно запущен!')
    except Exception:
        logger.exception('Проблема с подключением vk API')
        return

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        try:
            if event.type != VkEventType.MESSAGE_NEW:
                continue

            if not event.to_me:
                continue

            response = detect_intent_response(
                project_id,
                f'vk-{event.user_id}',
                event.text,
                language_code
            )

            if not response.query_result.intent.is_fallback:
                answer = response.query_result.fulfillment_text

                try:
                    vk.messages.send(
                        user_id=event.user_id,
                        message=answer,
                        random_id=0
                    )
                except ApiError:
                    continue

        except Exception:
            logger.exception('Ошибка при запуске бота!')
            continue


if __name__ == '__main__':
    load_dotenv()

    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    ))
    logger.addHandler(console_handler)

    error_tg_token = os.environ['ERROR_TELEGRAM_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']
    project_id = os.environ['PROJECT_GOOGLE_CLOUD_ID']
    language_code = os.getenv('LANGUAGE_CODE', 'ru-RU')
    vk_token = os.environ['VK_TOKEN']
    GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

    vk_error_handler = TelegramLogsHandler(error_tg_token, tg_chat_id)
    vk_error_handler.setLevel(logging.ERROR)
    vk_error_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    ))
    logger.addHandler(vk_error_handler)

    run_vk_bot(vk_token, project_id, language_code, error_tg_token, tg_chat_id)

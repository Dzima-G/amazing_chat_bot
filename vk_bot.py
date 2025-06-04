import logging

import vk_api
from telegram import Bot
from vk_api.exceptions import ApiError
from vk_api.longpoll import VkEventType, VkLongPoll

from dialog_flow_api import detect_intent_response
from tg_logging import TelegramLogsHandler


def run_vk_bot(vk_token, project_id, language_code, error_tg_token, tg_chat_id):
    logger = logging.getLogger('vk_logger')
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    ))
    logger.addHandler(console_handler)

    if error_tg_token and tg_chat_id:
        vk_error_handler = TelegramLogsHandler(error_tg_token, tg_chat_id)
        vk_error_handler.setLevel(logging.ERROR)
        vk_error_handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        ))
        logger.addHandler(vk_error_handler)

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
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    response = detect_intent_response(
                        project_id,
                        event.user_id,
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

import os
import threading

from dotenv import load_dotenv

from tg_bot import run_tg_bot
from vk_bot import run_vk_bot

if __name__ == '__main__':
    load_dotenv()

    tg_token = os.environ['TELEGRAM_TOKEN']
    error_tg_token = os.environ['ERROR_TELEGRAM_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']
    project_id = os.environ['PROJECT_GOOGLE_CLOUD_ID']
    language_code = os.getenv('LANGUAGE_CODE', 'ru-RU')
    vk_token = os.environ['VK_TOKEN']
    GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

    vk_thread = threading.Thread(
        target=run_vk_bot,
        args=(vk_token, project_id, language_code, error_tg_token, tg_chat_id),
        name="vk_thread",
        daemon=True
    )

    vk_thread.start()

    run_tg_bot(tg_token, project_id, language_code, error_tg_token, tg_chat_id)

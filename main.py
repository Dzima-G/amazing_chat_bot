import os
import threading

from dotenv import load_dotenv

from tg_bot import run_tg_bot
from vk_bot import run_vk_bot

if __name__ == '__main__':
    load_dotenv()

    tg_token = os.environ.get('TELEGRAM_TOKEN')
    project_id = os.environ.get('PROJECT_GOOGLE_CLOUD_ID')
    language_code = os.getenv('LANGUAGE_CODE', 'ru-RU')
    vk_token = os.getenv('VK_TOKEN')

    vk_thread = threading.Thread(
        target=run_vk_bot,
        args=(vk_token, project_id, language_code),
        name="vk_thread",
        daemon=True
    )

    vk_thread.start()

    run_tg_bot(tg_token, project_id, language_code)

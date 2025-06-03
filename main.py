import os

from dotenv import load_dotenv

from tg_bot import run_bot

if __name__ == '__main__':
    load_dotenv()

    tg_token = os.environ.get('TELEGRAM_TOKEN')
    project_id = os.environ.get('PROJECT_GOOGLE_CLOUD_ID')
    language_code = os.getenv('LANGUAGE_CODE', 'ru-RU')
    vk_token = os.getenv('VK_TOKEN')

    run_bot(tg_token=tg_token, project_id=project_id, language_code=language_code)

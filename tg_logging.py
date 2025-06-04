import logging
import traceback

import requests


class TelegramLogsHandler(logging.Handler):

    def __init__(self, error_tg_token: str, tg_chat_id: str):
        super().__init__(level=logging.ERROR)
        self.bot_token = error_tg_token
        self.chat_id = tg_chat_id
        self.api_url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage'

    def emit(self, record: logging.LogRecord):
        try:
            log_entry = self.format(record)
            if record.exc_info:
                tb_text = ''.join(traceback.format_exception(*record.exc_info))
                log_entry += '\n\n' + tb_text

            safe_text = (
                '*Ошибка в боте*'
                '```\n'
                f'{log_entry}'
                '\n```'
            )

            payload = {
                'chat_id': self.chat_id,
                'text': f'Бот упал с ошибкой:\n\n{safe_text}',
                'parse_mode': 'Markdown'
            }

            requests.post(self.api_url, data=payload, timeout=5)
        except Exception:
            pass

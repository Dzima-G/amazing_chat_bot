import logging

from telegram import Bot, ForceReply, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialog_flow_api import detect_intent_texts
from tg_logging import TelegramLogsHandler

logger = logging.getLogger('tg_logger')


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    try:
        project_id = context.bot_data.get('PROJECT_GOOGLE_CLOUD_ID')
        language_code = context.bot_data.get('LANGUAGE_CODE')

        answer = detect_intent_texts(
            project_id,
            update.message.from_user.id,
            update.message.text,
            language_code)

        update.message.reply_text(answer)
    except Exception:
        logger.exception('Ошибка при обработке текстового сообщения.')


def run_tg_bot(tg_token, project_id, language_code, error_tg_token, tg_chat_id) -> None:
    """Start the bot."""

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    if error_tg_token and tg_chat_id:
        tg_error_handler = TelegramLogsHandler(error_tg_token, tg_chat_id)
        tg_error_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
        tg_error_handler.setFormatter(formatter)
        logger.addHandler(tg_error_handler)

        tg_error_bot = Bot(token=error_tg_token)
        tg_error_bot.send_message(
            chat_id=tg_chat_id,
            text='Бот Telegram успешно запущен!'
        )

    updater = Updater(tg_token)

    dispatcher = updater.dispatcher
    dispatcher.bot_data['PROJECT_GOOGLE_CLOUD_ID'] = project_id
    dispatcher.bot_data['LANGUAGE_CODE'] = language_code

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    try:
        logger.info('Бот Telegram успешно запущен!')

        updater.start_polling()
        updater.idle()
    except Exception:
        logger.exception('Ошибка при запуске бота!')

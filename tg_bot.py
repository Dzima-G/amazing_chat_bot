import logging

from telegram import ForceReply, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialog_flow_api import detect_intent_texts

logger = logging.getLogger(__name__)


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

    project_id = context.bot_data.get('PROJECT_GOOGLE_CLOUD_ID')
    language_code = context.bot_data.get('LANGUAGE_CODE')

    answer = detect_intent_texts(
        project_id,
        update.message.from_user.id,
        update.message.text,
        language_code)

    update.message.reply_text(answer)


def run_bot(tg_token, project_id, language_code) -> None:
    """Start the bot."""

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    updater = Updater(tg_token)

    dispatcher = updater.dispatcher

    dispatcher.bot_data['PROJECT_GOOGLE_CLOUD_ID'] = project_id
    dispatcher.bot_data['LANGUAGE_CODE'] = language_code

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

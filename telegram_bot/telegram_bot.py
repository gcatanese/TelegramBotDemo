import time
import re
import pyfiglet
import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram

from _model import *


def get_chat_id(update, context):
    chat_id = -1

    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]

    return chat_id


def get_user(update):
    user: User = None

    _from = None

    if update.message is not None:
        _from = update.message.from_user
    elif update.callback_query is not None:
        _from = update.callback_query.from_user

    if _from is not None:
        user = User()
        user.id = _from.id
        user.first_name = _from.first_name if _from.first_name is not None else ''
        user.last_name = _from.last_name if _from.last_name is not None else ''
        user.lang = _from.language_code if _from.language_code is not None else 'n/a'

    logging.info(f'from {user}')

    return user


def help_command_handler(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Send me an hashtag (i.e. #saveOurPlanet) to see where it goes.')
    add_typing(update, context)
    update.message.reply_text('More info at https://myhashtag.app/')


def main_handler(update, context):
    logging.info(f'update : {update}')

    user_input = get_text(update)
    logging.info(f'user_input : {user_input}')

    if update.message is not None:
        # text message
        add_typing(update, context)
        add_text_message(update, context, "hey")

        # add_typing(update, context)
        # buttons = MultiItems("What do you think?", ["⭐", "⭐⭐", "⭐⭐⭐"])
        # add_suggested_actions(update, context, buttons)

        #add_document(update, context, "https://tweesky.com/logo.png")
    elif update.callback_query is not None:
        # callback
        add_typing(update, context)
        add_text_message(update, context, "hey")
    elif update.poll is not None:
        # poll
        None



def add_typing(update, context):
    context.bot.send_chat_action(chat_id=get_chat_id(update, context), action=telegram.ChatAction.TYPING, timeout=1)
    time.sleep(1)


def add_text_message(update, context, message):
    if update.message is not None:
        #context.bot.send_message(chat_id=get_chat_id(update, context), text=message)
        update.message.reply_text(message)
    elif update.callback_query is not None:

        update.callback_query.message.edit_text(message)

def add_suggested_actions(update, context, response):
    options = []

    for item in response.items:
        options.append(InlineKeyboardButton(item, callback_data=item))

    reply_markup = InlineKeyboardMarkup([options])

    context.bot.send_message(chat_id=get_chat_id(update, context), text=response.message, reply_markup=reply_markup)


def add_document(update, context, url):
    context.bot.send_document(chat_id=get_chat_id(update, context), document=url)

def get_text(update):
    return 'a' #update.message.text


def extract_hashtags(text):
    return re.findall(r"#(\w+)", text)


def error(update, context):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" ', update)
    logging.exception(context.error)


def get_user(update):
    user: User = None

    _from = None

    if update.message is not None:
        _from = update.message.from_user
    elif update.callback_query is not None:
        _from = update.callback_query.from_user

    if _from is not None:
        user = User()
        user.id = _from.id
        user.first_name = _from.first_name if _from.first_name is not None else ''
        user.last_name = _from.last_name if _from.last_name is not None else ''
        user.lang = _from.language_code if _from.language_code is not None else 'n/a'

    return user


def main():
    updater = Updater(DefaultConfig.TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher

    # cmd
    dp.add_handler(CommandHandler("help", help_command_handler))

    # message handler
    dp.add_handler(MessageHandler(Filters.text, main_handler))

    # suggested_actions_handler
    dp.add_handler(CallbackQueryHandler(main_handler, pass_chat_data=True, pass_user_data=True))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if DefaultConfig.MODE == 'webhook':

        updater.start_webhook(listen="0.0.0.0",
                              port=int(DefaultConfig.PORT),
                              url_path=DefaultConfig.TELEGRAM_TOKEN)
        updater.bot.setWebhook(DefaultConfig.WEBHOOK_URL + DefaultConfig.TELEGRAM_TOKEN)

        logging.info(f"Start webhook mode on port {DefaultConfig.PORT}")
    else:
        updater.start_polling()
        logging.info(f"Start polling mode")

    updater.idle()


class DefaultConfig:
    PORT = int(os.environ.get("PORT", 3978))
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
    MODE = os.environ.get("MODE", "polling")
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")

    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

    @staticmethod
    def init_logging():
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                            level=DefaultConfig.LOG_LEVEL)


if __name__ == '__main__':
    ascii_banner = pyfiglet.figlet_format("MyHashtag")
    print(ascii_banner)

    # Enable logging
    DefaultConfig.init_logging()

    main()

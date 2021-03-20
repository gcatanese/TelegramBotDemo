import time
import re
import pyfiglet
import logging
import logging.config
import os
import requests


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram

from _model import *

PORT = int(os.environ.get('PORT', '8443'))
logging.info(f'PORT {PORT}')


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


def start_command_handler(update, context):
    """Send a message when the command /start is issued."""
    add_typing(update, context)
    buttons = MultiItems("What would you like to receive?", ["Text", "File", "GoogleDoc", "Gallery"])
    add_suggested_actions(update, context, buttons)


def help_command_handler(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Type /start')


def main_handler(update, context):
    logging.info(f'update : {update}')

    if update.message is not None:
        user_input = get_text_from_message(update)
        logging.info(f'user_input : {user_input}')

        # reply
        add_typing(update, context)
        add_text_message(update, context, f"You said: {user_input}")

    elif update.callback_query is not None:
        user_input = get_text_from_callback(update)
        logging.info(f'user_input : {user_input}')

        if user_input == 'Simple Text':
            add_typing(update, context)
            add_text_message(update, context, "Hello from the Bot 😎")
        elif user_input == 'File':
            # file from Github
            url = "https://github.com/gcatanese/TelegramBotDemo/raw/main/files/test.pdf"
            add_document(update, context, url)
        elif user_input == 'GoogleDoc':
            # google doc
            url = "https://docs.google.com/document/d/10KPUejkqitf2lKHzNUreSO5TwlQ3XDwi_mb-CiAD8Zg/edit?usp=sharing"
            fetch_and_send(update, context, url)
        elif user_input == 'Gallery':
            send_gallery(update, context)


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


def fetch_and_send(update, context, url):
    r = requests.get(url, allow_redirects=True)
    print(r)
    open('googledoc.docx', 'wb').write(r.content)

    context.bot.send_document(chat_id=get_chat_id(update, context), document=open('googledoc.docx', 'rb'), filename="googledoc.docx")


def send_gallery(update, context):
    list = []

    list.append(InputMediaPhoto(media='https://github.com/gcatanese/TelegramBotDemo/raw/main/files/mintie.jpg', caption='Mint'))
    list.append(InputMediaPhoto(media='https://github.com/gcatanese/TelegramBotDemo/raw/main/files/pinkie.jpg', caption='Pink'))
    list.append(InputMediaPhoto(media='https://github.com/gcatanese/TelegramBotDemo/raw/main/files/orangie.jpg', caption='Orange'))

    context.bot.send_media_group(chat_id=get_chat_id(update, context), media=list)


def get_text_from_message(update):
    return update.message.text


def get_text_from_callback(update):
    return update.callback_query.data


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

    # command handlers
    dp.add_handler(CommandHandler("help", help_command_handler))
    dp.add_handler(CommandHandler("start", start_command_handler))

    # message handler
    dp.add_handler(MessageHandler(Filters.text, main_handler))

    # suggested_actions_handler
    dp.add_handler(CallbackQueryHandler(main_handler, pass_chat_data=True, pass_user_data=True))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if DefaultConfig.MODE == 'webhook':

        logging.info(f'PORT2 {PORT}')

        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=DefaultConfig.TELEGRAM_TOKEN)
        updater.bot.setWebhook(DefaultConfig.WEBHOOK_URL + DefaultConfig.TELEGRAM_TOKEN)

        logging.info(f"Start webhook mode on port {DefaultConfig.PORT}")
    else:
        updater.start_polling()
        logging.info(f"Start polling mode")

    #updater.idle()


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
        #logging.config.fileConfig('logging.conf')


if __name__ == '__main__':
    ascii_banner = pyfiglet.figlet_format("MyHashtag")
    print(ascii_banner)

    # Enable logging
    DefaultConfig.init_logging()

    main()

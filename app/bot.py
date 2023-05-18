import os
import sys

from config import (ABOUT_TEXT, ADMIN_IDS, AGENDA_TEXT, BOT_TOKEN, BUTTONS,
                    FYST_FEST_DB, GOT_MESSAGE, HELLO_TEXT, MENU_FILE,
                    MENU_MESSAGE, MESSAGE_QUESTION_TEXT, SCRIPT_FILE,
                    WRITE_MESSAGE)
from filters import BASE_MESSAGE_FILTERS
from sql_connector import SqlConnector
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, error
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, MessageHandler)
from utils import get_apply


async def send_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_counter = [0]
    user_id = update.callback_query.from_user.id
    bot = context.bot
    query = update.callback_query.data
    customers = SqlConnector.get_users_id()
    customers = list(customers).remove(user_id)
    text_message = query.split('__')[1]
    if customers:
        for cust_id in customers:
            try:
                await bot.send_message(cust_id, text=text_message)
                message_counter[0] += 1
                SqlConnector.set_user_state(user_id, True)
            except error.BadRequest:
                SqlConnector.set_user_state(user_id, False)
    admin_message = f'{message_counter[0]} {GOT_MESSAGE}'
    await bot.send_message(user_id, text=admin_message)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    await update.effective_chat.send_message(HELLO_TEXT)
    await main_menu(update, context)
    user = SqlConnector.get_user_id(user_id)
    if not user:
        SqlConnector.insert_user_id(user_id)


async def main_menu(update: Update,
                    context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [
        [
            KeyboardButton(BUTTONS['about']),
            KeyboardButton(BUTTONS['agenda'])
        ],
        [KeyboardButton(BUTTONS['menu'])],
        [KeyboardButton(BUTTONS['request_song'])],
        [KeyboardButton(BUTTONS['send_photo'])],
    ]
    chat_id = update.message.from_user.id
    if chat_id in ADMIN_IDS:
        buttons.append([KeyboardButton(BUTTONS['send_message'])])
    keyboard_markup = ReplyKeyboardMarkup(buttons)
    await context.bot.send_message(chat_id=chat_id, text='Choose one:',
                                   reply_markup=keyboard_markup)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    await context.bot.send_message(chat_id=user_id, text=ABOUT_TEXT)


async def agenda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    await context.bot.send_message(user_id=user_id, text=AGENDA_TEXT)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.from_user.id
    menu_doc = open(MENU_FILE, 'rb')
    await context.bot.send_message(chat_id=chat_id, text=MENU_MESSAGE)
    try:
        await context.bot.send_document(chat_id=chat_id, document=menu_doc)
    except error.TimedOut:
        pass


async def request_song():
    pass


async def send_photo():
    pass


async def any_message(update: Update,
                      context: ContextTypes.DEFAULT_TYPE) -> None:
    dialog_flag = False
    user_id = update.message.from_user.id
    if context.chat_data.get(user_id) and user_id in ADMIN_IDS:
        if context.chat_data[user_id] == "send_message":
            context.chat_data[user_id] = update.message.text
            await get_apply(update, context, MESSAGE_QUESTION_TEXT)
            dialog_flag = True
    if update.message.text == BUTTONS['about']:
        await about(update, context)
    elif update.message.text == BUTTONS['menu']:
        await menu(update, context)
    elif update.message.text == BUTTONS['agenda']:
        await agenda(update, context)
    elif update.message.text == BUTTONS['send_message']:
        if user_id in ADMIN_IDS:
            context.chat_data[user_id] = "send_message"
            await context.bot.send_message(user_id, WRITE_MESSAGE)
            dialog_flag = True
    if not dialog_flag:
        context.chat_data[user_id] = {}


async def handle_callback_query(update: Update,
                                context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query.data.split("__")[0]
    chat_id = update.callback_query.message.chat.id
    if query == "send":
        await send_messages(update, context)
    elif query == "delete":
        message_id = update.callback_query.message.message_id
        await context.bot.delete_message(chat_id, message_id)


def check_creds() -> bool:
    return all([
        os.path.exists(FYST_FEST_DB),
        BOT_TOKEN
    ])


def main():
    if not os.path.exists(FYST_FEST_DB):
        SqlConnector.create_database(FYST_FEST_DB, SCRIPT_FILE)
    if not check_creds():
        sys.exit()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(MessageHandler(BASE_MESSAGE_FILTERS, any_message))
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    application.run_polling()


if __name__ == '__main__':
    main()

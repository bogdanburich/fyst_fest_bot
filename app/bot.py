import sys

import os
from config import BOT_TOKEN, BUTTONS, HELLO_TEXT, ABOUT_TEXT, NIHT_PROGRAMM,\
    MENU_MESSAGE, USERS_ID
from filters import BASE_MESSAGE_FILTERS
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                        MessageHandler)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_message(HELLO_TEXT)
    await main_menu(update, context)


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
    
    user_id = update.message.from_user.id
    if user_id in USERS_ID:
        buttons.append([KeyboardButton(BUTTONS['send_message'])])
        
    keyboard_markup = ReplyKeyboardMarkup(buttons)

    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id,
                                text='Choose one:',
                                reply_markup=keyboard_markup)
    


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    await context.bot.send_message(chat_id=user_id, text=ABOUT_TEXT)


async def agenda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    context.chat_data[user_id] = "menu"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "static/menu.pdf")
    with open(file_path, "rb") as file:
        await context.bot.send_message(chat_id=user_id, text=MENU_MESSAGE)
        await context.bot.send_document(chat_id=user_id, document=file)

async def request_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    context.chat_data[user_id] = "request_song"

async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    context.chat_data[user_id] = "send_photo"


async def any_message(update: Update,
                    context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.chat_data:
        ...
    if update.message.text == BUTTONS['back']:
        await main_menu(update, context)
    elif update.message.text == BUTTONS['about']:
        await about(update, context)
    elif update.message.text == BUTTONS['agenda']:
        await agenda(update, context)
    elif update.message.text == BUTTONS['menu']:
        await menu(update, context)
    elif update.message.text == BUTTONS['request_song']:
        await request_song(update, context)

def check_creds() -> bool:
    return all([
        BOT_TOKEN
    ])


def main():
    if not check_creds():
        sys.exit()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(MessageHandler(BASE_MESSAGE_FILTERS, any_message))
    application.add_handler(CommandHandler('start', start))

    application.run_polling()


if __name__ == '__main__':
    main()

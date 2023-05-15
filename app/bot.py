import sys

from config import BOT_TOKEN, BUTTONS, HELLO_TEXT
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
    keyboard_markup = ReplyKeyboardMarkup(buttons)

    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id,
                                   text='Choose one:',
                                   reply_markup=keyboard_markup)


async def about():
    pass


async def agenda():
    pass


async def menu():
    pass


async def request_song():
    pass


async def send_photo():
    pass


async def any_message(update: Update,
                      context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.chat_data:
        pass
    if update.message.text == BUTTONS['back']:
        await main_menu(update, context)


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

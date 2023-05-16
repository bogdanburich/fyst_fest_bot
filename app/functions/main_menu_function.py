import sys
import os

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import (ContextTypes)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import BUTTONS, ADMIN_ID



async def main_menu_func(update: Update,
                    context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    context.chat_data[user_id] = {}
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
    if user_id in ADMIN_ID:
        buttons.append([KeyboardButton(BUTTONS['send_message'])])
        
    keyboard_markup = ReplyKeyboardMarkup(buttons)

    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id,
                                text='Choose one:',
                                reply_markup=keyboard_markup)
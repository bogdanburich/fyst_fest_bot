import json

from config import DELETE_TEXT, SEND_TEXT
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def forward_message(message, channel_id):
    pass


async def get_apply(update: Update, context: ContextTypes.DEFAULT_TYPE,
                    question_text: str, action: list):
    user_id = update.message.from_user.id
    print(user_id)
    users_text = update.message.text
    call = {
            'action': action[0],
            'message': users_text
            }
    call_del = {
                'action': action[1],
                }
    call = json.dumps(call)
    call_del = json.dumps(call_del)
    callback_button_send = InlineKeyboardButton(SEND_TEXT, callback_data=call)
    callback_button_delete = InlineKeyboardButton(DELETE_TEXT, callback_data=(
        call_del))
    keyboard = InlineKeyboardMarkup([[callback_button_send,
                                    callback_button_delete]])
    message = f'{question_text}\n{users_text}'
    await update.message.reply_text(message, reply_markup=keyboard)
    context.chat_data[user_id] = ''

import json
import os
import sys

from config import (ABOUT_TEXT, ADMIN_IDS, AGENDA_TEXT, BOT_TOKEN, BUTTONS,
                    DELETE_TEXT, ERRORS, FYST_FEST_DB, GOT_MESSAGE, HELLO_TEXT,
                    MAX_SONG_LENGTH, MENU_FILE, MENU_MESSAGE,
                    MESSAGE_QUESTION_TEXT, MUSIC_CHANNEL_ID, REQUEST_SONG_TEXT,
                    REQUESTED_SONG, SCRIPT_FILE, SEND_TEXT, WRITE_MESSAGE)
from filters import BASE_MESSAGE_FILTERS
from sql_connector import SqlConnector
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton, ReplyKeyboardMarkup, Update, error)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, MessageHandler)
from utils import is_admin


async def get_apply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_id = update.message.id
    users_text = update.message.text
    call = {'action': 'send_messages', 'message_id': message_id}
    call_del = {'action': 'delete'}
    call = json.dumps(call)
    call_del = json.dumps(call_del)
    callback_button_send = InlineKeyboardButton(SEND_TEXT, callback_data=call)
    callback_button_delete = InlineKeyboardButton(DELETE_TEXT,
                                                  callback_data=call_del)
    keyboard = InlineKeyboardMarkup([[callback_button_send,
                                      callback_button_delete]])
    message = f'{MESSAGE_QUESTION_TEXT}\n{users_text}'
    await update.message.reply_text(message, reply_markup=keyboard)
    del context.chat_data[user_id]


async def send_everyone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_counter = 0
    admin_id = update.callback_query.from_user.id
    bot = context.bot
    query = update.callback_query.data
    users_ids = list(SqlConnector.get_users_id())
    users_ids.remove(admin_id)
    message_id = json.loads(query)['message_id']
    for user_id in users_ids:
        try:
            await bot.forward_message(chat_id=user_id,
                                      from_chat_id=admin_id,
                                      message_id=message_id)
            message_counter += 1
        except error.BadRequest:
            SqlConnector.set_user_active(admin_id, False)
    admin_message = f'{message_counter} {GOT_MESSAGE}'
    await bot.send_message(admin_id, text=admin_message)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user = SqlConnector.get_user(user_id)
    if not user:
        SqlConnector.insert_or_activate_user(user_id)
    buttons = [
        [
            KeyboardButton(BUTTONS['about']),
            KeyboardButton(BUTTONS['agenda'])
        ],
        [KeyboardButton(BUTTONS['menu'])],
        [KeyboardButton(BUTTONS['request_song'])],
        [KeyboardButton(BUTTONS['send_photo'])],
    ]
    if user_id in ADMIN_IDS:
        buttons.append([KeyboardButton(BUTTONS['send_message'])])
    keyboard_markup = ReplyKeyboardMarkup(buttons)
    await context.bot.send_message(chat_id=user_id, text=HELLO_TEXT,
                                   reply_markup=keyboard_markup)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    await context.bot.send_message(chat_id=user_id, text=ABOUT_TEXT)


async def agenda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    await context.bot.send_message(chat_id=user_id, text=AGENDA_TEXT)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.from_user.id
    menu_doc = open(MENU_FILE, 'rb')
    await context.bot.send_message(chat_id=chat_id, text=MENU_MESSAGE)
    try:
        await context.bot.send_document(chat_id=chat_id, document=menu_doc)
    except error.TimedOut:
        pass


async def send_photo():
    pass


async def request_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user_id = update.message.from_user.id
    if len(message) >= MAX_SONG_LENGTH:
        await context.bot.send_message(chat_id=user_id,
                                       text=ERRORS['name_too_long'])
        return
    message_id = update.message.id
    await context.bot.forward_message(chat_id=MUSIC_CHANNEL_ID,
                                      from_chat_id=user_id,
                                      message_id=message_id)
    await context.bot.send_message(chat_id=user_id,
                                   text=REQUESTED_SONG)
    del context.chat_data[user_id]


async def context_handler(update: Update, context: ContextTypes.DEFAULT_TYPE,
                          user_id: int):
    if context.chat_data[user_id] == 'send_message' and is_admin(user_id):
        await get_apply(update, context)
    elif context.chat_data[user_id] == 'request_song':
        await request_song(update, context)


async def handler(update: Update,
                  context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    message = update.message.text

    if message not in BUTTONS.values() and context.chat_data.get(user_id):
        context_handler(update=update, context=context, user_id=user_id)

    if update.message.text == BUTTONS['about']:
        await about(update, context)
    elif update.message.text == BUTTONS['menu']:
        await menu(update, context)
    elif update.message.text == BUTTONS['agenda']:
        await agenda(update, context)
    elif update.message.text == BUTTONS['send_message']:
        if is_admin(user_id):
            context.chat_data[user_id] = 'send_message'
            await context.bot.send_message(user_id, WRITE_MESSAGE)
    elif update.message.text == BUTTONS['request_song']:
        context.chat_data[user_id] = 'request_song'
        await context.bot.send_message(user_id, REQUEST_SONG_TEXT)


async def callback_handler(update: Update,
                           context: ContextTypes.DEFAULT_TYPE):
    action = json.loads(update.callback_query.data)['action']
    chat_id = update.callback_query.message.chat.id
    if action == 'send_messages':
        await send_everyone(update, context)
    elif action == 'delete':
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

    application.add_handler(MessageHandler(BASE_MESSAGE_FILTERS, handler))
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(callback_handler))

    application.run_polling()


if __name__ == '__main__':
    main()

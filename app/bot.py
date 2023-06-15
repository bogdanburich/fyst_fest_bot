import json
import os
import sys

import httpx
import logs
import texts
from config import (ADMIN_IDS, BOT_TOKEN, BUTTONS, ERRORS, FYST_FEST_DB,
                    MAX_SONG_LENGTH, MUSIC_CHANNEL_ID, PHOTO_CHANNEL_ID,
                    SCRIPT_FILE)
from exceptions import ValidationError
from filters import BASE_MESSAGE_FILTERS
from sql_connector import SqlConnector
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton, ReplyKeyboardMarkup, Update, error)
from telegram.ext import (Application, CallbackQueryHandler, ChatMemberHandler,
                          CommandHandler, ContextTypes, MessageHandler)
from validators import is_admin, is_photo_valid

logger = logs.get_logger(__name__)


def set_context(context: ContextTypes.DEFAULT_TYPE, user_id: int, action: str):
    context.chat_data[user_id] = {'action': action}


async def error_handler(update: Update, context):
    e = context.error
    if isinstance(e, (httpx.HTTPError, error.NetworkError)):
        logger.warn(f'Network error {e.__class__}:{e} handled')
    else:
        raise e


async def send_error(update: Update, context: ContextTypes.DEFAULT_TYPE,
                     text: str):
    user_id = update.message.from_user.id
    await context.bot.send_message(chat_id=user_id,
                                   text=text)


async def deactivate_user(update: Update,
                          context: ContextTypes.DEFAULT_TYPE):
    user_id = update.my_chat_member.chat.id
    status = update.my_chat_member.new_chat_member.status
    if status == 'kicked':
        SqlConnector.set_user_inactive(user_id)


async def get_apply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_id = update.message.id

    send = json.dumps({'action': 'send', 'message_id': message_id})
    delete = json.dumps({'action': 'delete'})

    button_send = InlineKeyboardButton('✅ Send', callback_data=send)
    button_delete = InlineKeyboardButton('❌ Delete', callback_data=delete)
    keyboard = InlineKeyboardMarkup([[button_send, button_delete]])

    apply = 'Send message above?'
    await update.message.reply_text(apply, reply_markup=keyboard)

    del context.chat_data[user_id]


async def send_everyone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = update.callback_query.from_user.id
    user_ids = SqlConnector.get_user_ids()

    try:
        user_ids.remove(admin_id)
    except ValueError:
        pass

    query = update.callback_query.data
    message_id = json.loads(query)['message_id']

    message_counter = 0
    message_sent_ids = []
    for user_id in user_ids:
        try:
            await context.bot.forward_message(chat_id=user_id,
                                              from_chat_id=admin_id,
                                              message_id=message_id)
            message_counter += 1
            message_sent_ids.append(user_id)

        except error.Forbidden:
            SqlConnector.set_user_inactive(user_id)

    admin_message = f'{message_counter} people got message'
    await context.bot.send_message(admin_id, text=admin_message)
    logger.info(f'Message has been sent to {message_sent_ids}')


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
        # [KeyboardButton(BUTTONS['menu'])],
        [KeyboardButton(BUTTONS['request_song'])],
        [KeyboardButton(BUTTONS['send_photo'])],
    ]

    if user_id in ADMIN_IDS:
        buttons.append([KeyboardButton(BUTTONS['send_message'])])
        buttons.append([KeyboardButton(BUTTONS['stats'])])

    keyboard_markup = ReplyKeyboardMarkup(buttons)

    await context.bot.send_message(chat_id=user_id, text=texts.HELLO,
                                   parse_mode='html',
                                   reply_markup=keyboard_markup)
    logger.info(f'User {user_id} has started bot')


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    users_cnt = SqlConnector.users_count()
    message = f'{users_cnt} people activated bot'
    await context.bot.send_message(chat_id=user_id, text=message)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    await context.bot.send_message(chat_id=user_id,
                                   parse_mode='html',
                                   text=texts.ABOUT)


async def agenda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    await context.bot.send_message(chat_id=user_id,
                                   parse_mode='html',
                                   text=texts.AGENDA)


# async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = update.message.from_user.id
#     # menu_doc = open(MENU_FILE, 'rb')

#     # try:
#     #     await context.bot.send_document(chat_id=chat_id, document=menu_doc)
#     # except error.TimedOut:
#     #     pass
#     await context.bot.send_message(chat_id=user_id,
#                                    parse_mode='html',
#                                    text=texts.MENU,
#                                    disable_web_page_preview=True)


async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = update.message.id
    user_id = update.message.from_user.id

    if is_photo_valid(update, context):
        await context.bot.forward_message(chat_id=PHOTO_CHANNEL_ID,
                                          from_chat_id=user_id,
                                          message_id=message_id)
        await context.bot.send_message(chat_id=user_id,
                                       text='Photo has been sent')


async def request_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user_id = update.message.from_user.id
    message_id = update.message.id

    if len(message) >= MAX_SONG_LENGTH:
        await context.bot.send_message(chat_id=user_id,
                                       text=ERRORS['name_too_long'])
        return

    await context.bot.forward_message(chat_id=MUSIC_CHANNEL_ID,
                                      from_chat_id=user_id,
                                      message_id=message_id)
    await context.bot.send_message(chat_id=user_id,
                                   text='Song has been requested')

    del context.chat_data[user_id]


async def context_handler(update: Update, context: ContextTypes.DEFAULT_TYPE,
                          user_id: int):
    action = context.chat_data[user_id]['action']

    if action == 'send_message':
        await get_apply(update, context)
    elif action == 'request_song':
        await request_song(update, context)
    elif action == 'send_photo':
        await send_photo(update, context)


async def handler(update: Update,
                  context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    message = update.message.text
    user_context = context.chat_data.get(user_id)
    bot = context.bot

    try:

        if message not in BUTTONS.values() and user_context:
            await context_handler(update=update, context=context,
                                  user_id=user_id)
        elif user_context:
            del context.chat_data[user_id]

        if message == BUTTONS.get('about'):
            await about(update, context)
        # if message == BUTTONS.get('menu'):
        #     await menu(update, context)
        if message == BUTTONS.get('agenda'):
            await agenda(update, context)
        if message == BUTTONS.get('request_song'):
            set_context(context, user_id, 'request_song')
            await bot.send_message(user_id, 'Write your song:')
        if message == BUTTONS.get('send_photo'):
            set_context(context, user_id, 'send_photo')
            await bot.send_message(user_id, 'Send your photo:')

        if message == BUTTONS.get('send_message'):
            is_admin(user_id)
            set_context(context, user_id, 'send_message')
            await bot.send_message(user_id, 'Write your message:')
        if message == BUTTONS.get('stats'):
            is_admin(user_id)
            await stats(update, context)

    except ValidationError as e:

        await send_error(update, context, e.message)


async def callback_handler(update: Update,
                           context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id

    action = json.loads(update.callback_query.data)['action']
    if action == 'send':
        await context.bot.delete_message(chat_id, message_id)
        await send_everyone(update, context)
    elif action == 'delete':
        await context.bot.delete_message(chat_id, message_id)
        logger.info('Message has been deleted')


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

    logs.init_logging()

    application = (Application
                   .builder()
                   .token(BOT_TOKEN)
                   .build())

    application.add_handler(MessageHandler(BASE_MESSAGE_FILTERS, handler))
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(ChatMemberHandler(deactivate_user))
    application.add_error_handler(error_handler)

    application.run_polling()


if __name__ == '__main__':
    main()

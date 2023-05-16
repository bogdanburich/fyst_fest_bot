import sys

from config import BOT_TOKEN, BUTTONS, HELLO_TEXT, ABOUT_TEXT, ADMIN_ID, \
    WRITE_MESSAGE
from filters import BASE_MESSAGE_FILTERS
from telegram import Update

from telegram.ext import Application, CommandHandler, ContextTypes,\
    MessageHandler, CallbackQueryHandler

from functions.send_message_function import send_messages, get_apply
from functions.main_menu_function import main_menu_func
from functions.get_menu_function import get_pdf_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_message(HELLO_TEXT)
    await main_menu_func(update, context)

async def main_menu(update: Update,
                    context: ContextTypes.DEFAULT_TYPE) -> None:
    await main_menu_func(update, context)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    await context.bot.send_message(chat_id=user_id, text=ABOUT_TEXT)

async def agenda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ...

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await get_pdf_menu(update, context)

async def request_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ...

async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ...
    
async def send_apply(update: Update,
                    context: ContextTypes.DEFAULT_TYPE):
        await get_apply(update, context)

async def any_message(update: Update,
                    context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if context.chat_data.get(user_id) and user_id in ADMIN_ID:
        await send_apply(update, context)
        return
    elif update.message.text == BUTTONS['back']:
        await main_menu(update, context)
    elif update.message.text == BUTTONS['about']:
        await about(update, context)
    elif update.message.text == BUTTONS['agenda']:
        await agenda(update, context)
    elif update.message.text == BUTTONS['menu']:
        await menu(update, context)
    elif update.message.text == BUTTONS['request_song']:
        await request_song(update, context)
    elif update.message.text == BUTTONS['send_message']:
        if user_id in ADMIN_ID:
            context.chat_data[user_id] = "send_message"
            await context.bot.send_message(user_id, WRITE_MESSAGE)
            return
    await main_menu(update, context)
            
async def handle_callback_query(update: Update, context:
                                                    ContextTypes.DEFAULT_TYPE):
    query = update.callback_query.data.split("__")[0]
    if query =="send":
        await send_messages(update, context)
    elif query == "delete":
        chat_id = update.callback_query.message.chat.id
        message_id = update.callback_query.message.message_id
        await context.bot.delete_message(chat_id, message_id)

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
    application.add_handler(CallbackQueryHandler(handle_callback_query))


    application.run_polling()


if __name__ == '__main__':
    main()

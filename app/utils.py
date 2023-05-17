import os

from config import BASE_DIR, MENU_MESSAGE
from telegram import Update
from telegram.ext import ContextTypes


async def forward_message(message, channel_id):
    pass


async def get_pdf_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_path = os.path.join(BASE_DIR, "static")
    menu_path = os.path.join(menu_path, "menu.pdf")
    chat_id = update.message.from_user.id
    context.chat_data[chat_id] = "menu"
    menu_doc = open(menu_path, 'rb')
    try:
        await context.bot.send_message(chat_id=chat_id, text=MENU_MESSAGE)
        await context.bot.send_document(chat_id=chat_id, document=menu_doc)
    except Exception:
        ...

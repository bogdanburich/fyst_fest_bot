import os
from telegram import Update
from telegram.ext import ContextTypes
from config import MENU_MESSAGE, BASE_DIR


async def get_pdf_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_path = os.path.join(BASE_DIR, "static")
    menu_path = os.path.join(menu_path, "menu.pdf")
    chat_id = update.message.from_user.id
    context.chat_data[chat_id] = "menu"
    menu_doc = open(menu_path, 'rb')
    await context.bot.send_message(chat_id=chat_id, text=MENU_MESSAGE)
    await context.bot.send_document(chat_id, menu_doc)

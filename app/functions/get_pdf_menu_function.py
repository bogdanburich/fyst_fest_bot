import os
from telegram import Update
from telegram.ext import ContextTypes
from config import MENU_MESSAGE


async def get_pdf_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    menu_path = menu_path+"/static/menu.pdf"
    user_id = update.message.from_user.id
    context.chat_data[user_id] = "menu"
    with open(menu_path, "rb") as file:
        await context.bot.send_message(chat_id=user_id, text=MENU_MESSAGE)
        await context.bot.send_document(chat_id=user_id, document=file)

import sys
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import ADMIN_ID




async def send_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    customer_counter = 0
    user_id = update.callback_query.from_user.id
    bot = context.bot
    query = update.callback_query.data
    text_message = query.split("__")[1]
    for customer_id in context.chat_data:
        if customer_id not in ADMIN_ID:
            customer_counter = await try_send_message(customer_counter, 
                                                bot, customer_id, text_message)
    admin_message = f"{customer_counter} people got message"
    await bot.send_message(user_id, text=admin_message)

async def try_send_message(customer_counter:int, bot:ContextTypes.DEFAULT_TYPE,
                        customer_id:int, text_message:str):
    try:
        await bot.send_message(customer_id, text=text_message)
        customer_counter = customer_counter + 1
        return customer_counter
    except:
        return customer_counter
    
    
async def get_apply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if context.chat_data[user_id] == "send_message":
            context.chat_data[user_id] = update.message.text
            message_text = context.chat_data[user_id]
            callback_button_send = InlineKeyboardButton("Send",
                                        callback_data=f"send__{message_text}")
            callback_button_delete = InlineKeyboardButton("Delete",
                                                    callback_data="delete__")
            keyboard = InlineKeyboardMarkup([[callback_button_send, 
                                            callback_button_delete]])
            await update.message.reply_text(f"Send message?:\n'{message_text}'"
                                            , reply_markup=keyboard)
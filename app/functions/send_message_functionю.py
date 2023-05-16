from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import ADMIN_ID


async def send_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    customer_counter = 0
    user_id = update.callback_query.from_user.id
    bot = context.bot
    query = update.callback_query.data
    text_message = query.split("__")[1]
    for customer_id in context.chat_data:
        if customer_id not in ADMIN_ID:
            customer_counter = await try_send_message(customer_counter, bot,
                                                      customer_id,
                                                      text_message)
    admin_message = f"{customer_counter} people got message"
    await bot.send_message(user_id, text=admin_message)


async def try_send_message(customer_counter: int, bot: ContextTypes.
                           DEFAULT_TYPE, customer_id: int, text_message: str):
    try:
        await bot.send_message(customer_id, text=text_message)
        customer_counter = customer_counter + 1
        return customer_counter
    except Exception():
        return customer_counter


async def get_apply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if context.chat_data[user_id] == "send_message":
        context.chat_data[user_id] = update.message.text
        message_text = context.chat_data[user_id]
        call = f"send__{message_text}"
        call_del = "delete__"
        callback_button_send = InlineKeyboardButton("Send", callback_data=call)
        callback_button_delete = InlineKeyboardButton("Delete", callback_data=(
            call_del))
        keyboard = InlineKeyboardMarkup([[callback_button_send,
                                        callback_button_delete]])
        message = f"Send message?:\n'{message_text}'"
        await update.message.reply_text(message, reply_markup=keyboard)

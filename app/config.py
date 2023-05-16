import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv("env_file.env")

BASE_DIR = str(Path(__file__).resolve().parent)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

ERRORS = {
}

ADMIN_IDS = [
]

PHOTO_CHANNEL_ID = ''

SONG_CHANNEL_ID = ''

HELLO_TEXT = 'Hello'

AGENDA_TEXT = 'Agenda'

MENU_FILE = os.path.join(BASE_DIR, 'static/menu.pdf')

BUTTONS = {
    'about': 'ℹ️ About',
    'agenda': '🔖 Agenda',
    'menu': '🍕 Menu',
    'request_song': '🎵 Request Song',
    'send_photo': '📷 Send Photo',
    'back': '🔙 Back',
    'send_message': '📝 Send message',
}


ABOUT_TEXT = """ 
🔖 Agenda - Get a program for today

🍕 Menu - Get the menu

🎵 Request Song - Order music

📷 Send Photo - Send a photo
"""

MENU_MESSAGE = "One moment..."

NIHT_PROGRAMM = "tuz tuz tuz"

ADMIN_ID = [402816936]

WRITE_MESSAGE = "Write your message..."

CANCEL_DIALOG = "Dialog was send"
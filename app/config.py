import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = str(Path(__file__).resolve().parent)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

ERRORS = {
}

ADMIN_IDS = [
    116553777,
]

PHOTO_CHANNEL_ID = -1916305987

MUSIC_CHANNEL_ID = -1904676592

HELLO_TEXT = 'Hello'

AGENDA_TEXT = 'Agenda'

MENU_FILE = os.path.join(BASE_DIR, 'static/menu.pdf')

BUTTONS = {
    'about': 'ℹ️ About',
    'agenda': '🔖 Agenda',
    'menu': '🍕 Menu',
    'request_song': '🎵 Request Song',
    'send_photo': '📷 Send Photo',
    'back': '🔙 Back'
}

ABOUT_TEXT = '''
🔖 Agenda - Get a program for today

🍕 Menu - Get the menu

🎵 Request Song - Order music

📷 Send Photo - Send a photo
'''

MENU_MESSAGE = 'One moment...'

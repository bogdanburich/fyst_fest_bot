import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = str(Path(__file__).resolve().parent)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

ERRORS = {
}

ADMIN_IDS = [
    116553777, 402816936, 295699541
]

PHOTO_CHANNEL_ID = -1916305987

MUSIC_CHANNEL_ID = -1904676592

HELLO_TEXT = 'Hello\nChoose one:'

AGENDA_TEXT = 'Agenda'

MENU_FILE = os.path.join(BASE_DIR, 'static/menu.pdf')

BUTTONS = {
    'about': 'ℹ️ About',
    'agenda': '🔖 Agenda',
    'menu': '🍕 Menu',
    'request_song': '🎵 Request Song',
    'send_photo': '📷 Send Photo',
    'send_message': '📝 Send message'
}

ABOUT_TEXT = '''
🔖 Agenda - Get a program for today

🍕 Menu - Get the menu

🎵 Request Song - Order music

📷 Send Photo - Send a photo
'''

MENU_MESSAGE = 'One moment...'

WRITE_MESSAGE = 'Write your message...'

SEND_TEXT = '✅ Send'

DELETE_TEXT = '❌ Delete'

SEND_QUESTION = 'Send message?:\n'

GOT_MESSAGE = 'people got message'

DATABASE_NAME = 'fyst_fest.db'

SCRIPT_FILE_NAME = "CREATE_TABLE_users.sql"

SCRIPT_FILE = os.path.join(BASE_DIR, "migrations")

SCRIPT_FILE = os.path.join(SCRIPT_FILE, SCRIPT_FILE_NAME)

FYST_FEST_DB = os.path.join(BASE_DIR, DATABASE_NAME)

MESSAGE_QUESTION_TEXT = "Send message?\n"

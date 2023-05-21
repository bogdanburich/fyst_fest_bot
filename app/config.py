import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = str(Path(__file__).resolve().parent)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

ERRORS = {
    'name_too_long': 'Name is too long, try again:',
    'not_photo': 'It is not photo...'
    }

ADMIN_IDS = [
    116553777, 402816936, 295699541
]

PHOTO_CHANNEL_ID = -1001916305987

MUSIC_CHANNEL_ID = -1001904676592

MENU_FILE = os.path.join(BASE_DIR, 'static/menu.pdf')

BUTTONS = {
    'about': 'ℹ️ About',
    'agenda': '🔖 Agenda',
    'menu': '🍕 Menu',
    'request_song': '🎵 Request Song',
    'send_photo': '📷 Send Photo',
    'send_message': '📝 Send message'
}

DATABASE_NAME = 'fyst_fest.db'

SCRIPT_FILE_NAME = 'CREATE_TABLE_users.sql'

SCRIPT_FILE = os.path.join(BASE_DIR, 'migrations', SCRIPT_FILE_NAME)

FYST_FEST_DB = os.path.join(BASE_DIR, DATABASE_NAME)

MAX_SONG_LENGTH = 100

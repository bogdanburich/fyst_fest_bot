import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = str(Path(__file__).resolve().parent)

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'DEV')

BOT_TOKEN = os.environ.get('BOT_TOKEN')

ERRORS = {
    'name_too_long': 'Name is too long, try again:',
    'not_photo': 'It is not photo, try again:',
    'photo_group': 'One photo per message, try again:',
    'not_allowed': 'You\'re not allowed to perform this action'
}

ADMIN_IDS = (
    116553777,
    218190566,
    406122043,
    451930808,
    137967905,
    443924742,
    295699541
)

PHOTO_CHANNEL_ID = -1001916305987

MUSIC_CHANNEL_ID = -1001904676592

# MENU_FILE = os.path.join(BASE_DIR, 'static/menu.pdf')

BUTTONS = {
    'about': 'ℹ️ About',
    'agenda': '🔖 Agenda',
    # 'menu': '🍕 Menu',
    'request_song': '🎵 Request Song (after-party)',
    'send_photo': '📷 Send Photo',
    'send_message': '📝 Send message',
    'stats': '📊 Stats'
}

DATABASE_NAME = 'fyst_fest.db'

SCRIPT_FILE_NAME = 'CREATE_TABLE_users.sql'

SCRIPT_FILE = os.path.join(BASE_DIR, 'migrations', SCRIPT_FILE_NAME)

FYST_FEST_DB = os.path.join(BASE_DIR, DATABASE_NAME)

MAX_SONG_LENGTH = 32

SENTRY_DSN = os.environ.get('SENTRY_DSN')

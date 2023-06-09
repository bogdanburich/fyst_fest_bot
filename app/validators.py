from config import ADMIN_IDS, ERRORS
from exceptions import ValidationError


def is_admin(user_id):
    if user_id not in ADMIN_IDS:
        raise ValidationError(ERRORS['not_allowed'])


def is_photo_valid(update, context) -> bool:
    message = update.message
    user_id = message.from_user.id

    if message.media_group_id:
        context_media_group_id = (context.chat_data[user_id]
                                  .get('media_group_id'))
        if context_media_group_id == message.media_group_id:
            return False
        context.chat_data[user_id]['media_group_id'] = message.media_group_id
        raise ValidationError(ERRORS['photo_group'])
    if not message.photo:
        raise ValidationError(ERRORS['not_photo'])

    return True

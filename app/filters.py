from telegram.ext import filters


class MessageFilter(filters.MessageFilter):
    def filter(self, message):
        return (
            not message.new_chat_members and not message.left_chat_member
        )


BASE_MESSAGE_FILTERS = (~filters.COMMAND
                        & ~filters.UpdateType.EDITED_MESSAGE
                        & MessageFilter())

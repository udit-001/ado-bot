from telegram.ext import BaseFilter


class FilterUsernameRec(BaseFilter):
    def filter(self, message):
        if bool(message.reply_to_message):
            return 'Okay, then! Now send me your name of your cute creature so that I can finish up this process, and send you the avatar.' == message.reply_to_message.text

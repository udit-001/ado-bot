from telegram import ChatAction
from telegram.ext import MessageHandler

from util.filters import FilterUsernameRec

filter_usernameRec = FilterUsernameRec()


def username_received(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
    bot.sendPhoto(chat_id=update.message.chat_id, photo='http://api.adorable.io/avatars/'+update.message.text,
                  reply_to_message_id=update.message.message_id, caption='Here\'s your little {0}!'.format(update.message.text.capitalize()))


def register(dp):
    dp.add_handler(MessageHandler(filter_usernameRec, username_received))
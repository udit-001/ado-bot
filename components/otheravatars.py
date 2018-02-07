from telegram import InputTextMessageContent, InlineQueryResultPhoto
from telegram.ext import InlineQueryHandler


def dis_heads_inline_query(bot, update, user_data):
    chat_id = user_data['config']['create_chat_id']
    msg_id = user_data['config']['create_message_id']

    query = update.inline_query.query
    username = query.split("dis_heads")[1].strip()

    if username:
        msg = InputTextMessageContent(message_text=username)
        results = [InlineQueryResultPhoto(type='photo', id=k, photo_url='https://robohash.org/{0}?set=set3&bgset=bg{1}&size=500x500'.format(username,k),thumb_url='https://robohash.org/{0}?set=set3&bgset=bg{1}&size=500x500'.format(username, k), input_message_content=msg) for k in ('1', '2')]
        bot.answerInlineQuery(update.inline_query.id, results=results)
    else:
        bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="Okay, then! Now send me the name of your disembodied head so that I can finish up this process, and send you the avatar.\n\nExample : `@avatarGenBot dis_heads john`", parse_mode="Markdown")


def kitten_inline_query(bot, update, user_data):
    chat_id = user_data['config']['create_chat_id']
    msg_id = user_data['config']['create_message_id']

    query = update.inline_query.query
    username = query.split("kitten")[1].strip()

    if username:
        msg = InputTextMessageContent(message_text=username)
        results = [InlineQueryResultPhoto(type='photo', id=k, photo_url='https://robohash.org/{0}?set=set4&bgset=bg{1}&size=500x500'.format(username, k), thumb_url='https://robohash.org/{0}?set=set4&bgset=bg{1}&size=500x500'.format(username, k), input_message_content=msg) for k in ('1', '2')]
        bot.answerInlineQuery(update.inline_query.id, results=results)
    else:
        bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="Okay, then! Now send me the name of your cute kitty, so that I can finish up this process, and send you the avatar.\n\nExample : `@avatarGenBot kitten fluffy`", parse_mode="Markdown")


def robot_inline_query(bot, update, user_data):
    chat_id = user_data['config']['create_chat_id']
    msg_id = user_data['config']['create_message_id']

    query = update.inline_query.query
    username = query.split("robot")[1].strip()

    if username:
        msg = InputTextMessageContent(message_text=username)
        results = [InlineQueryResultPhoto(type='photo', id=k, photo_url='https://robohash.org/{0}?set=set1&bgset=bg{1}&size=500x500'.format(username,k),thumb_url='https://robohash.org/{0}?set=set1&bgset=bg{1}&size=500x500'.format(username,k),input_message_content=msg) for k in ('1','2')]
        bot.answerInlineQuery(update.inline_query.id, results=results)
    else:
        bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="Okay, then! Now send me the name of your robot, so that I can finish up this process, and send you the avatar.\n\nExample : `@avatarGenBot robot alfred`",parse_mode="Markdown")


def monster_inline_query(bot, update, user_data):
    chat_id = user_data['config']['create_chat_id']
    msg_id = user_data['config']['create_message_id']

    query = update.inline_query.query
    username = query.split("monster")[1].strip()

    if username:
        msg = InputTextMessageContent(message_text=username)
        results = [InlineQueryResultPhoto(type='photo', id=k, photo_url='https://robohash.org/{0}?set=set2&bgset=bg{1}&size=500x500'.format(username,k),thumb_url='https://robohash.org/{0}?set=set2&bgset=bg{1}&size=500x500'.format(username,k),input_message_content=msg) for k in ('1','2')]
        bot.answerInlineQuery(update.inline_query.id, results=results)
    else:
        bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="Okay, then! Now send me the name of your monster, so that I can finish up this process, and send you the avatar.\n\nExample : `@avatarGenBot monster frankenstein`",parse_mode="Markdown")


def register(dp):
    dp.add_handler(InlineQueryHandler(dis_heads_inline_query, pattern="dis_heads", pass_user_data=True))
    dp.add_handler(InlineQueryHandler(kitten_inline_query, pattern="kitten", pass_user_data=True))
    dp.add_handler(InlineQueryHandler(robot_inline_query, pattern="robot", pass_user_data=True))
    dp.add_handler(InlineQueryHandler(monster_inline_query, pattern="monster", pass_user_data=True))
from telegram import InlineQueryResultPhoto, InputTextMessageContent, InlineQueryResultArticle
from telegram.ext import InlineQueryHandler

from util.hexcode import find_hex


def eyes_inline_query(bot, update):

    results = [InlineQueryResultPhoto(type='photo', id=k, photo_url='https://raw.githubusercontent.com/udit-001/ado-bot/master/assets/eyes/eyes{0}.png'.format(str(k)), thumb_url='https://raw.githubusercontent.com/udit-001/ado-bot/master/assets/eyes/eyes{0}.png'.format(str(k)), input_message_content=InputTextMessageContent(message_text='eyes{0}'.format(str(k)))) for k in (1, 10, 2, 3, 4, 5, 6, 7, 9)]

    bot.answerInlineQuery(update.inline_query.id, results=results)


def mouth_inline_query(bot,update):
    results = [InlineQueryResultPhoto(type='photo', id=k, photo_url='https://raw.githubusercontent.com/udit-001/ado-bot/master/assets/mouth/mouth{0}.png'.format(str(k)), thumb_url='https://raw.githubusercontent.com/udit-001/ado-bot/master/assets/mouth/mouth{0}.png'.format(str(k)), input_message_content=InputTextMessageContent(message_text='mouth{0}'.format(str(k)))) for k in (1, 10, 11, 3, 5, 6, 7, 9)]

    bot.answerInlineQuery(update.inline_query.id, results=results)


def nose_inline_query(bot, update):
    results = [InlineQueryResultPhoto(type='photo', id=k, photo_url='https://raw.githubusercontent.com/udit-001/ado-bot/master/assets/nose/nose{0}.png'.format(str(k)), thumb_url='https://raw.githubusercontent.com/udit-001/ado-bot/master/assets/nose/nose{0}.png'.format(str(k)), input_message_content=InputTextMessageContent(message_text='nose{0}'.format(str(k)))) for k in (2, 3, 4, 5, 6, 7, 8, 9)]

    bot.answerInlineQuery(update.inline_query.id, results=results)


def color_inline_query(bot, update):
    query = update.inline_query.query

    color = query.split("color")[1].strip()

    if color:
        hex_color = find_hex(color)
        msg = InputTextMessageContent(message_text=hex_color)
        results = [InlineQueryResultArticle(type='article', id=hex_color, title=color.capitalize(), thumb_url='http://img.dummy-image-generator.com/_mono/dummy-200x200-color{0}-plain.jpg'.format(hex_color), input_message_content=msg)]
        bot.answerInlineQuery(update.inline_query.id, results=results)

    else:
        results = [InlineQueryResultPhoto(type='photo', id=k, photo_url='http://img.dummy-image-generator.com/_mono/dummy-200x200-color{0}-plain.jpg'.format(str(k)), thumb_url='http://img.dummy-image-generator.com/_mono/dummy-200x200-color{0}-plain.jpg'.format(str(k)), photo_height=100, photo_width=100, input_message_content=InputTextMessageContent(message_text='{0}'.format(str(k)))) for k in ('EF5350', 'F44336', 'E53935', 'EC407A', 'E91E63', 'D81B60', 'AB47BC', '9C27B0', '8E24AA', '7E57C2', '673AB7', '5E35B1', '5C6BC0', '3F51B5', '3949AB','42A5F5','2196F3','1E88E5','26A69A','009688','00897B','81C784','66BB6A','4CAF50','9CCC65','8BC34A','7CB342','FFEE58','FFEB3B','FDD835','FF7043','FF5722','F4511E','8D6E63','795548','6D4C41','BDBDBD','9E9E9E','757575','90A4AE','78909C','607D8B')]
        bot.answerInlineQuery(update.inline_query.id, results=results)


def register(dp):
    dp.add_handler(InlineQueryHandler(eyes_inline_query, pattern="eyes"))
    dp.add_handler(InlineQueryHandler(nose_inline_query, pattern="nose"))
    dp.add_handler(InlineQueryHandler(mouth_inline_query, pattern="mouth"))
    dp.add_handler(InlineQueryHandler(color_inline_query, pattern="color"))

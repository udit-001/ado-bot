from telegram import InlineQueryResultPhoto, InlineQueryResultCachedPhoto, InputTextMessageContent, InlineQueryResultArticle
from telegram.ext import InlineQueryHandler
from util.hexcode import find_hex
from util.decorators import feedback_timer
import config


@feedback_timer
def eyes_inline_query(bot, update, user_data, job_queue):
    eyes = config.eyes

    results = [InlineQueryResultCachedPhoto(type='photo', id=item[0], photo_file_id=item[1],
                                            input_message_content=InputTextMessageContent(
                                                message_text='eyes{0}'.format(str(item[0])))) for item in
               eyes.items()]

    bot.answerInlineQuery(update.inline_query.id, results=results)


@feedback_timer
def mouth_inline_query(bot, update, user_data, job_queue):
    mouth = config.mouth

    results = [InlineQueryResultCachedPhoto(type='photo', id=item[0], photo_file_id=item[1],
                                            input_message_content=InputTextMessageContent(
                                                message_text='mouth{0}'.format(str(item[0])))) for item in
               mouth.items()]

    bot.answerInlineQuery(update.inline_query.id, results=results)


@feedback_timer
def nose_inline_query(bot, update, user_data, job_queue):
    nose = config.nose

    results = [InlineQueryResultCachedPhoto(type='photo', id=item[0], photo_file_id=item[1],
                                            input_message_content=InputTextMessageContent(
                                                message_text='nose{0}'.format(str(item[0])))) for item in
               nose.items()]

    bot.answerInlineQuery(update.inline_query.id, results=results)


@feedback_timer
def color_inline_query(bot, update, user_data, job_queue):
    colors = config.colors

    query = update.inline_query.query

    color = query.split("color")[1].strip()

    if color:
        hex_color = find_hex(color)
        msg = InputTextMessageContent(message_text=hex_color)
        results = [InlineQueryResultArticle(type='article', id=hex_color, title=color.capitalize(), thumb_url='http://img.dummy-image-generator.com/_mono/dummy-200x200-color{0}-plain.jpg'.format(hex_color), input_message_content=msg)]
        bot.answerInlineQuery(update.inline_query.id, results=results)

    else:
        results = [InlineQueryResultCachedPhoto(type='photo', id=item[0], photo_file_id=item[1], input_message_content=InputTextMessageContent(message_text='{0}'.format(str(item[0])))) for item in colors.items()]
        bot.answerInlineQuery(update.inline_query.id, results=results)


def register(dp):
    dp.add_handler(InlineQueryHandler(eyes_inline_query, pattern="eyes", pass_job_queue=True, pass_user_data=True))
    dp.add_handler(InlineQueryHandler(nose_inline_query, pattern="nose", pass_job_queue=True, pass_user_data=True))
    dp.add_handler(InlineQueryHandler(mouth_inline_query, pattern="mouth", pass_job_queue=True, pass_user_data=True))
    dp.add_handler(InlineQueryHandler(color_inline_query, pattern="color", pass_job_queue=True, pass_user_data=True))

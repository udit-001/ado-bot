# -*- coding: utf-8 -*-
import logging
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, InlineQueryResultPhoto, \
    InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, CallbackQueryHandler, BaseFilter, MessageHandler, InlineQueryHandler, \
    ChosenInlineResultHandler
from telegram.ext import Updater

import config

BOT_TOKEN = config.BOT_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class FilterUsernameRec(BaseFilter):
    def filter(self, message):
        if bool(message.reply_to_message):
            return 'Okay, then! Now send me your name of your cute creature so that I can finish up this process, and send you the avatar.' == message.reply_to_message.text


filter_usernameRec = FilterUsernameRec()


def start(bot, update):
    username = update.message.from_user.first_name
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text='Hi '+username+', I can help you in creating an avatar for your bot or yourself in seconds try using /create.',reply_to_message_id=update.message.message_id)


def findHex(color):
    ua = UserAgent()
    URL = 'https://alexbeals.com/projects/colorize/search.php?q='
    headers = {'User-Agent':str(ua.random)}

    source = requests.get(URL+color,headers=headers)
    plain_text = source.text
    soup = BeautifulSoup(plain_text,'lxml')

    hex = soup.body.get('style').split(':')[1].strip()
    hex = hex.replace('#', '')
    return hex


def sendHexCode(bot, update, args):
    color = args[0]
    hexColor = findHex(color)
    bot.send_chat_action(chat_id=update.message.chat_id,action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id,text=hexColor,reply_to_message_id=update.message.message_id)
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
    bot.sendPhoto(chat_id=update.message.chat_id,photo='http://img.dummy-image-generator.com/_mono/dummy-200x200-color{0}-plain.jpg'.format(hexColor),reply_to_message_id=update.message.message_id)


def createMenu(bot,update,user_data):
    user_data.setdefault("config",{})
    keyboard = [[InlineKeyboardButton('Cute Creatures',callback_data='adorables'),InlineKeyboardButton('Disembodied Heads',switch_inline_query_current_chat='dis_heads ')],[InlineKeyboardButton('Cute Kittens',switch_inline_query_current_chat='kitten '),InlineKeyboardButton('Robots',switch_inline_query_current_chat='robot '),InlineKeyboardButton('Monsters',switch_inline_query_current_chat='monster ')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    m = bot.send_message(chat_id=update.message.chat_id,text='I can create the following kinds of avatars 🎭 for you!',reply_markup=reply_markup,reply_to_message_id=update.message.message_id)
    user_data['config']['create_chat_id'] = m.chat_id
    user_data['config']['create_message_id'] = m.message_id


def createMenuButtons(bot, update, user_data):
    query = update.callback_query
    user_data.setdefault("config",{})

    if query.data == 'adorables':
        buttons = [[InlineKeyboardButton("Using identifier",callback_data='username'),InlineKeyboardButton("Create Custom",callback_data='custom')],[InlineKeyboardButton("Back ⬅️",callback_data='backButton')]]
        reply_markup = InlineKeyboardMarkup(buttons)
        bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.TYPING)
        bot.edit_message_text(text='So, there are two ways by which we can create our cute creatures, by using username or identifier, or by using custom settings, choose the appropriate option from below, to start!',chat_id = query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup)

    if query.data == 'backButton':
        keyboard = [[InlineKeyboardButton('Cute Creatures',callback_data='adorables'),InlineKeyboardButton('Disembodied Heads',switch_inline_query_current_chat="dis_heads ")],[InlineKeyboardButton('Cute Kittens',switch_inline_query_current_chat="kitten "),InlineKeyboardButton('Robots',switch_inline_query_current_chat='robot '),InlineKeyboardButton('Monsters',switch_inline_query_current_chat='monster ')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.TYPING)
        bot.edit_message_text(chat_id=query.message.chat_id,text='I can create the following kinds of avatars 🎭 for you!',reply_markup=reply_markup,message_id=query.message.message_id)

    if query.data == 'custom':
        user_data['config'] = dict()
        user_data['config'].setdefault('custom_message_id',query.message.message_id)
        user_data['config'].setdefault('custom_message_chat_id',query.message.chat_id)

        keyboard = [[InlineKeyboardButton("Eyes",switch_inline_query_current_chat="eyes "),InlineKeyboardButton("Nose",switch_inline_query_current_chat="nose "),InlineKeyboardButton("Mouth",switch_inline_query_current_chat="mouth ")],[InlineKeyboardButton("Color",switch_inline_query_current_chat="color "),InlineKeyboardButton("Back ⬅️",callback_data="adorables")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_chat_action(chat_id=query.message.chat_id,action=ChatAction.TYPING)
        bot.edit_message_text(text='You can select different options for eyes, nose, mouth and color, to create your own custom avatar. Press appropriate buttons below to proceed.',chat_id=query.message.chat_id,message_id=query.message.message_id,reply_markup=reply_markup)

    if query.data == 'create':
        url = 'http://api.adorable.io/avatars/face/{0}/{1}/{2}/{3}'.format(user_data['config']['eyes'],user_data['config']['nose'],user_data['config']['mouth'],user_data['config']['color'])

        bot.edit_message_text(text='Your avatar has been created successfully! Check it out ☺️. Create more using /create',chat_id=query.message.chat_id,message_id=query.message.message_id)
        bot.send_chat_action(chat_id=query.message.chat_id,action=ChatAction.UPLOAD_PHOTO)
        bot.sendPhoto(chat_id=query.message.chat_id,photo=url,reply_to_message_id=query.message.message_id)


def eyesInlineQuery(bot, update):
    # stickers = {1:'CAADBQADDgADH4bQV3gye5od01QvAg', 10:'CAADBQADDwADH4bQV4F84uAxsx7RAg', 2:'CAADBQADEAADH4bQVzPpXmKZc4BxAg', 3:'CAADBQADEQADH4bQV6aBEKZB1NZqAg', 4:'CAADBQADEgADH4bQV4Xn3TVTy2IBAg', 5:'CAADBQADEwADH4bQV83aozUBEf6sAg', 6:'CAADBQADFAADH4bQV2XGD-Q7Va7nAg', 7:'CAADBQADFQADH4bQV1GeQHFlnBdZAg', 9:'CAADBQADFgADH4bQV3bW84N01hA8Ag'}
    # results = list()

    # for i in stickers.items():
    #     results.append(InlineQueryResultCachedSticker(type='sticker',id=i[0],sticker_file_id=i[1]))

    results = [InlineQueryResultPhoto(type='photo', id=k, photo_url='https://raw.githubusercontent.com/udit-001/ado-bot/master/assets/eyes/eyes{0}.png'.format(str(k)), thumb_url='https://raw.githubusercontent.com/udit-001/ado-bot/master/assets/eyes/eyes{0}.png'.format(str(k)),input_message_content=InputTextMessageContent(message_text='eyes{0}'.format(str(k)))) for k in (1,10,2,3,4,5,6,7,9)]

    bot.answerInlineQuery(update.inline_query.id, results=results)


def mouthInlineQuery(bot,update):
    results = [InlineQueryResultPhoto(type='photo', id=k, photo_url='https://raw.githubusercontent.com/udit-001/ado-bot/master/assets/mouth/mouth{0}.png'.format(str(k)), thumb_url='https://raw.githubusercontent.com/udit-001/ado-bot/master/assets/mouth/mouth{0}.png'.format(str(k)),input_message_content=InputTextMessageContent(message_text='mouth{0}'.format(str(k)))) for k in (1,10,11,3,5,6,7,9)]

    bot.answerInlineQuery(update.inline_query.id, results=results)


def noseInlineQuery(bot, update):
    results = [InlineQueryResultPhoto(type='photo', id=k, photo_url='https://raw.githubusercontent.com/udit-001/ado-bot/master/assets/nose/nose{0}.png'.format(str(k)), thumb_url='https://raw.githubusercontent.com/udit-001/ado-bot/master/assets/nose/nose{0}.png'.format(str(k)),input_message_content=InputTextMessageContent(message_text='nose{0}'.format(str(k)))) for k in (2,3,4,5,6,7,8,9)]

    bot.answerInlineQuery(update.inline_query.id,results=results)


def colorInlineQuery(bot, update):
    query = update.inline_query.query

    color = query.split("color")[1].strip()

    if color:
        hex = findHex(color)
        msg = InputTextMessageContent(message_text=hex)
        results = [InlineQueryResultArticle(type='article', id=hex, title=color.capitalize(), thumb_url='http://img.dummy-image-generator.com/_mono/dummy-200x200-color{0}-plain.jpg'.format(hex), input_message_content=msg)]
        bot.answerInlineQuery(update.inline_query.id, results=results)

    else:
        results = [InlineQueryResultPhoto(type='photo', id=k, photo_url='http://img.dummy-image-generator.com/_mono/dummy-200x200-color{0}-plain.jpg'.format(str(k)), thumb_url='http://img.dummy-image-generator.com/_mono/dummy-200x200-color{0}-plain.jpg'.format(str(k)), photo_height=100, photo_width=100, input_message_content=InputTextMessageContent(message_text='{0}'.format(str(k)))) for k in ('EF5350', 'F44336', 'E53935', 'EC407A', 'E91E63', 'D81B60', 'AB47BC', '9C27B0', '8E24AA', '7E57C2', '673AB7', '5E35B1', '5C6BC0', '3F51B5', '3949AB','42A5F5','2196F3','1E88E5','26A69A','009688','00897B','81C784','66BB6A','4CAF50','9CCC65','8BC34A','7CB342','FFEE58','FFEB3B','FDD835','FF7043','FF5722','F4511E','8D6E63','795548','6D4C41','BDBDBD','9E9E9E','757575','90A4AE','78909C','607D8B')]
        bot.answerInlineQuery(update.inline_query.id, results=results)


def dis_headsInlineQuery(bot, update, user_data):
    chatId = user_data['config']['create_chat_id']
    msgId = user_data['config']['create_message_id']

    query = update.inline_query.query
    username = query.split("dis_heads")[1].strip()

    if username:
        msg = InputTextMessageContent(message_text=username)
        results = [InlineQueryResultPhoto(type='photo', id=k, photo_url='https://robohash.org/{0}?set=set3&bgset=bg{1}&size=500x500'.format(username,k),thumb_url='https://robohash.org/{0}?set=set3&bgset=bg{1}&size=500x500'.format(username,k),input_message_content=msg) for k in ('1','2')]
        bot.answerInlineQuery(update.inline_query.id, results=results)
    else:
        bot.edit_message_text(chat_id=chatId, message_id=msgId, text="Okay, then! Now send me the name of your disembodied head so that I can finish up this process, and send you the avatar.\n\nExample : `@avatarGenBot dis_heads john`",parse_mode="Markdown")


def kittenInlineQuery(bot, update, user_data):
    chatId = user_data['config']['create_chat_id']
    msgId = user_data['config']['create_message_id']

    query = update.inline_query.query
    username = query.split("kitten")[1].strip()

    if username:
        msg = InputTextMessageContent(message_text=username)
        results = [InlineQueryResultPhoto(type='photo', id=k, photo_url='https://robohash.org/{0}?set=set4&bgset=bg{1}&size=500x500'.format(username, k), thumb_url='https://robohash.org/{0}?set=set4&bgset=bg{1}&size=500x500'.format(username, k), input_message_content=msg) for k in ('1', '2')]
        bot.answerInlineQuery(update.inline_query.id, results=results)
    else:
        bot.edit_message_text(chat_id=chatId, message_id=msgId, text="Okay, then! Now send me the name of your cute kitty, so that I can finish up this process, and send you the avatar.\n\nExample : `@avatarGenBot kitten fluffy`", parse_mode="Markdown")


def robotInlineQuery(bot, update, user_data):
    chatId = user_data['config']['create_chat_id']
    msgId = user_data['config']['create_message_id']

    query = update.inline_query.query
    username = query.split("robot")[1].strip()

    if username:
        msg = InputTextMessageContent(message_text=username)
        results = [InlineQueryResultPhoto(type='photo', id=k, photo_url='https://robohash.org/{0}?set=set1&bgset=bg{1}&size=500x500'.format(username,k),thumb_url='https://robohash.org/{0}?set=set1&bgset=bg{1}&size=500x500'.format(username,k),input_message_content=msg) for k in ('1','2')]
        bot.answerInlineQuery(update.inline_query.id, results=results)
    else:
        bot.edit_message_text(chat_id=chatId, message_id=msgId, text="Okay, then! Now send me the name of your robot, so that I can finish up this process, and send you the avatar.\n\nExample : `@avatarGenBot robot alfred`",parse_mode="Markdown")


def monsterInlineQuery(bot, update, user_data):
    chatId = user_data['config']['create_chat_id']
    msgId = user_data['config']['create_message_id']

    query = update.inline_query.query
    username = query.split("monster")[1].strip()

    if username:
        msg = InputTextMessageContent(message_text=username)
        results = [InlineQueryResultPhoto(type='photo', id=k, photo_url='https://robohash.org/{0}?set=set2&bgset=bg{1}&size=500x500'.format(username,k),thumb_url='https://robohash.org/{0}?set=set2&bgset=bg{1}&size=500x500'.format(username,k),input_message_content=msg) for k in ('1','2')]
        bot.answerInlineQuery(update.inline_query.id, results=results)
    else:
        bot.edit_message_text(chat_id=chatId, message_id=msgId, text="Okay, then! Now send me the name of your monster, so that I can finish up this process, and send you the avatar.\n\nExample : `@avatarGenBot monster frankenstein`",parse_mode="Markdown")


def adorablesMenuButtons(bot, update):
    query = update.callback_query

    if query.data == 'username':
        bot.send_message(text='Okay, then! Now send me your name of your cute creature so that I can finish up this process, and send you the avatar.', chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=ForceReply())


def sendInline(bot, update):
    if update.inline_query is not None and update.inline_query.query:
        query = update.inline_query.query

        bot.sendPhoto(chat_id=update.message.chat_id,photo='http://api.adorable.io/avatars//'+name, reply_to_message_id=update.message.message_id)


def handle(bot, update, user_data):
    user_data.setdefault('config',{})
    query = update['chosen_inline_result']['query']
    resultId = update['chosen_inline_result']['result_id']

    if 'eyes' in query:
        user_data['config'].setdefault('eyes','eyes'+resultId)
        
    if 'mouth' in query:
        user_data['config'].setdefault('mouth','mouth'+resultId)

    if 'nose' in query:
        user_data['config'].setdefault('nose','nose'+resultId)

    if 'color' in query:
        user_data['config'].setdefault('color',resultId)

    if user_data['config'].get('custom_message_id',0):

        eyes = user_data['config'].get("eyes","Not selected yet!")
        color = user_data['config'].get("color","Not selected yet!")
        nose = user_data["config"].get("nose","Not selected yet!")
        mouth = user_data["config"].get("mouth", "Not selected yet!")

        buttons = []
        for k in ('eyes', 'nose', 'mouth', 'color'):
            if k not in user_data['config']:
                buttons.append(k)
            else:
                pass

        if len(buttons) == 0:
            keyboard = [[InlineKeyboardButton('Create',callback_data='create')],[InlineKeyboardButton('Reset 🔃',callback_data='custom')]]
        else:
            keyboard = [[InlineKeyboardButton(s.capitalize(),switch_inline_query_current_chat = s+' ') for s in buttons],[InlineKeyboardButton('Reset 🔃',callback_data='custom')]]
    
        reply_markup = InlineKeyboardMarkup(keyboard)
    
        bot.edit_message_text(text="So far, your configuration for your custom avatar is :\n*Eyes* : `{0}`\n*Nose* : `{1}`\n*Mouth* : `{2}`\n*Color* : `{3}`".format(eyes,nose,mouth,color),chat_id=user_data['config']['custom_message_chat_id'],message_id=user_data['config']['custom_message_id'],parse_mode="Markdown",reply_markup=reply_markup)

    elif 'robot' in query:
        username = query.split('robot')[1].strip()
        resultID = update.chosen_inline_result.result_id
        bot.send_chat_action(chat_id=update.effective_user.id, action=ChatAction.UPLOAD_PHOTO)
        bot.edit_message_text(text='Your robot has been manufactured successfully! Go and test it out!☺️. Create more using /create',chat_id=user_data['config']['create_chat_id'],message_id=user_data['config']['create_message_id'])
        bot.sendPhoto(chat_id=update.effective_user.id,photo='https://robohash.org/{0}?set=set1&bgset=bg{1}&size=500x500'.format(username,resultID),caption='Here\'s your little {0}! 🤖'.format(username.capitalize()))

    elif 'dis_heads' in query:
        username = query.split('dis_heads')[1].strip()
        resultID = update.chosen_inline_result.result_id
        bot.send_chat_action(chat_id=update.effective_user.id, action=ChatAction.UPLOAD_PHOTO)
        bot.edit_message_text(text='Your avatar has been created successfully! Check it out ☺️. Create more using /create',chat_id=user_data['config']['create_chat_id'],message_id=user_data['config']['create_message_id'])
        bot.sendPhoto(chat_id=update.effective_user.id,photo='https://robohash.org/{0}?set=set3&bgset=bg{1}&size=500x500'.format(username,resultID),caption='Here\'s your little {0}! 😛'.format(username.capitalize()))

    elif 'kitten' in query:
        username = query.split('kitten')[1].strip()
        resultID = update.chosen_inline_result.result_id
        bot.send_chat_action(chat_id=update.effective_user.id, action=ChatAction.UPLOAD_PHOTO)
        bot.edit_message_text(text='Your kitty has been summoned successfully! Go and pet it!☺️. Create more using /create',chat_id=user_data['config']['create_chat_id'],message_id=user_data['config']['create_message_id'])
        bot.sendPhoto(chat_id=update.effective_user.id,photo='https://robohash.org/{0}?set=set4&bgset=bg{1}&size=500x500'.format(username,resultID),caption='Here\'s your cute little {0}! 😛'.format(username.capitalize()))

    elif 'monster' in query:
        username = query.split('monster')[1].strip()
        resultID = update.chosen_inline_result.result_id
        bot.send_chat_action(chat_id=update.effective_user.id, action=ChatAction.UPLOAD_PHOTO)
        bot.edit_message_text(text='Your monster has been summoned successfully! Go and pet it!☺️. Create more using /create',chat_id=user_data['config']['create_chat_id'],message_id=user_data['config']['create_message_id'])
        bot.sendPhoto(chat_id=update.effective_user.id,photo='https://robohash.org/{0}?set=set2&bgset=bg{1}&size=500x500'.format(username,resultID),caption='Here\'s your {0}! Don\'t worry he\'s friendly 👹'.format(username.capitalize()))

    pprint(update.to_dict())
    # pprint(user_data['config'])


def usernameRec(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
    bot.sendPhoto(chat_id=update.message.chat_id, photo='http://api.adorable.io/avatars/'+update.message.text, reply_to_message_id=update.message.message_id, caption='Here\'s your little {0}!'.format(update.message.text.capitalize()))


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(token=BOT_TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('color', sendHexCode, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('create', createMenu, pass_user_data=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(adorablesMenuButtons), group=1)
    updater.dispatcher.add_handler(CallbackQueryHandler(createMenuButtons, pass_user_data=True))
    updater.dispatcher.add_handler(InlineQueryHandler(eyesInlineQuery, pattern="eyes"))
    updater.dispatcher.add_handler(InlineQueryHandler(mouthInlineQuery, pattern="mouth"))
    updater.dispatcher.add_handler(InlineQueryHandler(noseInlineQuery, pattern="nose"))
    updater.dispatcher.add_handler(InlineQueryHandler(colorInlineQuery, pattern="color"))
    updater.dispatcher.add_handler(InlineQueryHandler(dis_headsInlineQuery, pattern="dis_heads", pass_user_data=True))
    updater.dispatcher.add_handler(InlineQueryHandler(kittenInlineQuery, pattern="kitten", pass_user_data=True))
    updater.dispatcher.add_handler(InlineQueryHandler(robotInlineQuery, pattern="robot", pass_user_data=True))
    updater.dispatcher.add_handler(InlineQueryHandler(monsterInlineQuery, pattern="monster", pass_user_data=True))
    updater.dispatcher.add_handler(ChosenInlineResultHandler(handle, pass_user_data=True))
    updater.dispatcher.add_handler(MessageHandler(filter_usernameRec, usernameRec))
    updater.dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
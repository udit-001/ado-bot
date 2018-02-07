# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, ChatAction
from telegram.ext import CallbackQueryHandler


def adorables_menu_buttons(bot, update):
    query = update.callback_query

    if query.data == 'username':
        bot.send_message(text='Okay, then! Now send me your name of your cute creature so that I can finish up this process, and send you the avatar.', chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=ForceReply())


def create_menu_buttons(bot, update, user_data):
    query = update.callback_query
    user_data.setdefault("config",{})

    if query.data == 'adorables':
        buttons = [[InlineKeyboardButton("Using identifier", callback_data='username'), InlineKeyboardButton("Create Custom", callback_data='custom')], [InlineKeyboardButton("Back ⬅️", callback_data='backButton')]]
        reply_markup = InlineKeyboardMarkup(buttons)
        bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.TYPING)
        bot.edit_message_text(text='So, there are two ways by which we can create our cute creatures, by using username or identifier, or by using custom settings, choose the appropriate option from below, to start!',chat_id = query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup)

    if query.data == 'backButton':
        keyboard = [[InlineKeyboardButton('Cute Creatures', callback_data='adorables'), InlineKeyboardButton('Disembodied Heads', switch_inline_query_current_chat="dis_heads ")], [InlineKeyboardButton('Cute Kittens', switch_inline_query_current_chat="kitten "), InlineKeyboardButton('Robots', switch_inline_query_current_chat='robot '), InlineKeyboardButton('Monsters', switch_inline_query_current_chat='monster ')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.TYPING)
        bot.edit_message_text(chat_id=query.message.chat_id,text='I can create the following kinds of avatars 🎭 for you!',reply_markup=reply_markup,message_id=query.message.message_id)

    if query.data == 'custom':
        user_data['config'] = dict()
        user_data['config'].setdefault('custom_message_id',query.message.message_id)
        user_data['config'].setdefault('custom_message_chat_id',query.message.chat_id)

        keyboard = [[InlineKeyboardButton("Eyes", switch_inline_query_current_chat="eyes "), InlineKeyboardButton("Nose", switch_inline_query_current_chat="nose "), InlineKeyboardButton("Mouth", switch_inline_query_current_chat="mouth ")], [InlineKeyboardButton("Color", switch_inline_query_current_chat="color "), InlineKeyboardButton("Back ⬅️", callback_data="adorables")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_chat_action(chat_id=query.message.chat_id,action=ChatAction.TYPING)
        bot.edit_message_text(text='You can select different options for eyes, nose, mouth and color, to create your own custom avatar. Press appropriate buttons below to proceed.', chat_id=query.message.chat_id, message_id=query.message.message_id,reply_markup=reply_markup)

    if query.data == 'create':
        url = 'http://api.adorable.io/avatars/face/{0}/{1}/{2}/{3}'.format(user_data['config']['eyes'],user_data['config']['nose'],user_data['config']['mouth'], user_data['config']['color'])

        bot.edit_message_text(text='Your avatar has been created successfully! Check it out ☺. Create more using /create', chat_id=query.message.chat_id, message_id=query.message.message_id)
        bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
        bot.sendPhoto(chat_id=query.message.chat_id, photo=url, reply_to_message_id=query.message.message_id)


def register(dp):
    dp.add_handler(CallbackQueryHandler(adorables_menu_buttons), group=1)
    dp.add_handler(CallbackQueryHandler(create_menu_buttons, pass_user_data=True))

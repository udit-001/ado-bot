# -*- coding: utf-8 -*-
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler

from util.hexcode import find_hex


def start(bot, update):
    username = update.message.from_user.first_name
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text='Hi {0} I can help you in creating an avatar for your bot or yourself in seconds try using /create.'.format(username), reply_to_message_id=update.message.message_id)


def send_hexcode(bot, update, args):
    color = args[0]
    hexcolor = find_hex(color)
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text=hexcolor, reply_to_message_id=update.message.message_id)
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
    bot.sendPhoto(chat_id=update.message.chat_id, photo='http://img.dummy-image-generator.com/_mono/dummy-200x200-color{0}-plain.jpg'.format(hexcolor), reply_to_message_id=update.message.message_id)


def create_menu(bot, update, user_data):
    user_data.setdefault("config", {})
    keyboard = [[InlineKeyboardButton('Cute Creatures', callback_data='adorables'), InlineKeyboardButton('Disembodied Heads', switch_inline_query_current_chat='dis_heads ')],[InlineKeyboardButton('Cute Kittens', switch_inline_query_current_chat='kitten '), InlineKeyboardButton('Robots', switch_inline_query_current_chat='robot '), InlineKeyboardButton('Monsters', switch_inline_query_current_chat='monster ')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    m = bot.send_message(chat_id=update.message.chat_id, text='I can create the following kinds of avatars 🎭 for you!', reply_markup=reply_markup, reply_to_message_id=update.message.message_id)
    user_data['config']['create_chat_id'] = m.chat_id
    user_data['config']['create_message_id'] = m.message_id


def register(dp):
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("color", send_hexcode, pass_user_data=True))
    dp.add_handler(CommandHandler("create", create_menu, pass_user_data=True))
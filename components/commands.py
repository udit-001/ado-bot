from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler
from util.hexcode import find_hex
from localization import gettext_from_update
from util.decorators import feedback_timer
from util.dashbot import track_user


@feedback_timer
def start(bot, update, user_data, job_queue):
    track_user(update)
    _ = gettext_from_update(update)
    username = update.message.from_user.first_name
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text=_('Hi {0} 👋, I can help you in creating an avatar for your bot or yourself in seconds try using /create.').format(username), reply_to_message_id=update.message.message_id)


@feedback_timer
def send_hexcode(bot, update, args, user_data, job_queue):
    if args:
        color = args[0]
        hexcolor = find_hex(color)
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        bot.send_message(chat_id=update.message.chat_id, text=hexcolor, reply_to_message_id=update.message.message_id)
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
        bot.sendPhoto(chat_id=update.message.chat_id,
                      photo='http://img.dummy-image-generator.com/_mono/dummy-200x200-color{0}-plain.jpg'.format(
                          hexcolor), reply_to_message_id=update.message.message_id)
    else:
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        bot.send_message(chat_id=update.message.chat_id, text='You haven\'t passed me any color yet.\n\n Example : `/color yellow`', reply_to_message_id=update.message.message_id, parse_mode="Markdown")


@feedback_timer
def create_menu(bot, update, user_data, job_queue):
    _ = gettext_from_update(update)
    user_data['config'] = dict()
    keyboard = [[InlineKeyboardButton(_('Cute Creatures'), callback_data='adorables'), InlineKeyboardButton(_('Disembodied Heads 🗣️'), switch_inline_query_current_chat='dis_heads ')],[InlineKeyboardButton(_('Cute Kittens 😺'), switch_inline_query_current_chat='kitten '), InlineKeyboardButton(_('Robots 🤖'), switch_inline_query_current_chat='robot '), InlineKeyboardButton(_('Monsters 👹'), switch_inline_query_current_chat='monster ')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    m = bot.send_message(chat_id=update.message.chat_id, text=_('I can create the following kinds of avatars 👤 for you!'),
                         reply_markup=reply_markup, reply_to_message_id=update.message.message_id)
    user_data['config'].setdefault('create_chat_id', m.chat_id)
    user_data['config'].setdefault('create_message_id', m.message_id)


@feedback_timer
def get_records(bot, update, user_data, job_queue):
    _ = gettext_from_update(update)
    check = {'kittens': _('Cute Kittens 😺'), 'monsters': _('Monsters 👹'), 'dis_heads': _('Disembodied Heads 🗣️'), 'robots': _('Robots 🤖'),'cute':'Cute Creatures'}
    avatars = list()

    for i in user_data.keys():
        if i in check.keys():
            avatars.append((i, check[i]))

    if len(avatars) == 0:
        msg = _('Sorry 😔, but you haven\'t created any avatars yet.')
    else:
        msg = _('Here is a list of avatars 👤 you have created till now:\n')
        for avatar in avatars:
            msg += '\n<b>{0}</b> -\n'.format(avatar[1].capitalize())
            for i in range(len(user_data[avatar[0]])):
                if i == (len(user_data[avatar[0]])-1):
                    msg += '  └ '+user_data[avatar[0]][i].capitalize()+'\n'
                else:
                    msg += '  ├ ' + user_data[avatar[0]][i].capitalize() + '\n'

    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text=msg, reply_to_message_id=update.message.message_id, parse_mode="HTML")


def rate_me(bot, update):
    _ = gettext_from_update(update)
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text=_('If you liked my services, rate me 5 stars at https://telegram.me/storebot?start=avatarGenbot\n\nHave a query and suggestion for the developer, message at @batman071'),
                     reply_to_message_id=update.message.message_id, disable_web_page_preview=True)


def register(dp):
    dp.add_handler(CommandHandler("start", start, pass_user_data=True, pass_job_queue=True))
    dp.add_handler(CommandHandler("color", send_hexcode, pass_args=True, pass_user_data=True, pass_job_queue=True))
    dp.add_handler(CommandHandler("create", create_menu, pass_user_data=True, pass_job_queue=True))
    dp.add_handler(CommandHandler("list", get_records, pass_user_data=True, pass_job_queue=True))
    dp.add_handler(CommandHandler("rate", rate_me))

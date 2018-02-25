from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, ChatAction
from telegram.ext import CallbackQueryHandler
from localization import gettext_from_update
from util.decorators import feedback_timer


@feedback_timer
def create_menu_buttons(bot, update, user_data, job_queue):
    query = update.callback_query
    user_data.setdefault("config", {})
    _ = gettext_from_update(update)

    if query.data == 'adorables':
        buttons = [[InlineKeyboardButton(_("Using identifier"), switch_inline_query_current_chat='username'), InlineKeyboardButton(_("Create Custom"), callback_data='custom')], [InlineKeyboardButton(_("Back ⬅️"), callback_data='backButton')]]
        reply_markup = InlineKeyboardMarkup(buttons)
        bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.TYPING)
        bot.edit_message_text(text=_('So, there are two ways by which we can create our cute creatures, by using username or identifier, or by using custom settings, choose the appropriate option from below, to start!'),chat_id = query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup)

    if query.data == 'backButton':
        keyboard = [[InlineKeyboardButton(_('Cute Creatures'), callback_data='adorables'), InlineKeyboardButton(_('Disembodied Heads 🗣️'), switch_inline_query_current_chat="dis_heads ")], [InlineKeyboardButton(_('Cute Kittens 😺'), switch_inline_query_current_chat="kitten "), InlineKeyboardButton(_('Robots 🤖'), switch_inline_query_current_chat='robot '), InlineKeyboardButton(_('Monsters 👹'), switch_inline_query_current_chat='monster ')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.TYPING)
        bot.edit_message_text(chat_id=query.message.chat_id, text=_('I can create the following kinds of avatars for you!'),reply_markup=reply_markup,message_id=query.message.message_id)

    if query.data == 'custom':
        user_data['config'] = dict()
        user_data['config'].setdefault('custom_message_id', query.message.message_id)
        user_data['config'].setdefault('custom_message_chat_id', query.message.chat_id)

        keyboard = [[InlineKeyboardButton(_("Eyes 👀"), switch_inline_query_current_chat="eyes "), InlineKeyboardButton(_("Nose 👃"), switch_inline_query_current_chat="nose "), InlineKeyboardButton(_("Mouth 👄"), switch_inline_query_current_chat="mouth ")], [InlineKeyboardButton(_("Color"), switch_inline_query_current_chat="color "), InlineKeyboardButton(_("Back ⬅️"), callback_data="adorables")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_chat_action(chat_id=query.message.chat_id,action=ChatAction.TYPING)
        bot.edit_message_text(text=_('You can select different options for eyes, nose, mouth and color, to create your own custom avatar. Press appropriate buttons below to proceed.'), chat_id=query.message.chat_id, message_id=query.message.message_id,reply_markup=reply_markup)

    if query.data == 'create':
        url = 'http://api.adorable.io/avatars/face/{0}/{1}/{2}/{3}'.format(user_data['config']['eyes'], user_data['config']['nose'], user_data['config']['mouth'], user_data['config']['color'])

        bot.edit_message_text(text=_('Your avatar has been created successfully! Check it out. Create more using /create'), chat_id=query.message.chat_id, message_id=query.message.message_id)
        bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
        bot.sendPhoto(chat_id=query.message.chat_id, photo=url, reply_to_message_id=query.message.message_id)


def register(dp):
    dp.add_handler(CallbackQueryHandler(create_menu_buttons, pass_user_data=True, pass_job_queue=True))

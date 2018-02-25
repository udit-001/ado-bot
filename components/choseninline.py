from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from telegram.ext import ChosenInlineResultHandler
from localization import gettext_from_update
from util.decorators import feedback_timer


@feedback_timer
def chosen_inline_manager(bot, update, user_data, job_queue):
    _ = gettext_from_update(update)
    user_data.setdefault('config', {})
    query = update['chosen_inline_result']['query']
    result_id = update['chosen_inline_result']['result_id']

    if 'eyes' in query:
        user_data['config'].setdefault('eyes', 'eyes' + result_id)

    if 'mouth' in query:
        user_data['config'].setdefault('mouth', 'mouth' + result_id)

    if 'nose' in query:
        user_data['config'].setdefault('nose', 'nose' + result_id)

    if 'color' in query:
        user_data['config'].setdefault('color', result_id)

    if user_data['config'].get('custom_message_id', 0):

        eyes = user_data['config'].get("eyes", _("Not selected yet!"))
        color = user_data['config'].get("color", _("Not selected yet!"))
        nose = user_data["config"].get("nose", _("Not selected yet!"))
        mouth = user_data["config"].get("mouth", _("Not selected yet!"))

        buttons = []
        for k in ('eyes', 'nose', 'mouth', 'color'):
            if k not in user_data['config']:
                buttons.append(k)
            else:
                pass

        if len(buttons) == 0:
            keyboard = [[InlineKeyboardButton(_('Create'), callback_data='create')],
                        [InlineKeyboardButton(_('Reset 🔃'), callback_data='custom')]]
        else:
            keyboard = [
                [InlineKeyboardButton(s.capitalize(), switch_inline_query_current_chat=s + ' ') for s in buttons],
                [InlineKeyboardButton(_('Reset 🔃'), callback_data='custom')]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        bot.edit_message_text(
            text=_("So far, your configuration for your custom avatar 👤 is :\n*Eyes* : `{0}`\n*Nose* : `{1}`\n*Mouth* : `{2}`\n*Color* : `{3}`").format(
                eyes, nose, mouth, color), chat_id=user_data['config']['custom_message_chat_id'],
            message_id=user_data['config']['custom_message_id'], parse_mode="Markdown", reply_markup=reply_markup)

    elif 'robot' in query:
        user_data.setdefault('robots', list())
        username = query.split('robot')[1].strip()
        user_data['robots'].append(username)
        result_id = update.chosen_inline_result.result_id
        bot.send_chat_action(chat_id=update.effective_user.id, action=ChatAction.UPLOAD_PHOTO)
        bot.edit_message_text(
            text=_('Your robot 🤖 has been manufactured successfully! Go and test it out!. Create more using /create'),
            chat_id=user_data['config']['create_chat_id'], message_id=user_data['config']['create_message_id'])
        bot.sendPhoto(chat_id=update.effective_user.id,
                      photo='https://robohash.org/{0}?set=set1&bgset=bg{1}&size=500x500'.format(username, result_id),
                      caption=_('Here\'s your little {0}!').format(username.capitalize()), timeout=60)

    elif 'dis_heads' in query:
        user_data.setdefault('dis_heads', list())
        username = query.split('dis_heads')[1].strip()
        user_data['dis_heads'].append(username)
        result_id = update.chosen_inline_result.result_id
        bot.send_chat_action(chat_id=update.effective_user.id, action=ChatAction.UPLOAD_PHOTO)
        bot.edit_message_text(
            text=_('Your avatar 👤 has been created successfully! Check it out. Create more using /create'),
            chat_id=user_data['config']['create_chat_id'], message_id=user_data['config']['create_message_id'])
        bot.sendPhoto(chat_id=update.effective_user.id,
                      photo='https://robohash.org/{0}?set=set3&bgset=bg{1}&size=500x500'.format(username, result_id),
                      caption=_('Here\'s your little {0}!').format(username.capitalize()), timeout=60)

    elif 'kitten' in query:
        user_data.setdefault('kittens', list())
        username = query.split('kitten')[1].strip()
        user_data['kittens'].append(username)
        result_id = update.chosen_inline_result.result_id
        bot.send_chat_action(chat_id=update.effective_user.id, action=ChatAction.UPLOAD_PHOTO)
        bot.edit_message_text(
            text=_('Your kitty 🐱 has been summoned successfully! Go and pet it! Create more using /create'),
            chat_id=user_data['config']['create_chat_id'], message_id=user_data['config']['create_message_id'])
        bot.sendPhoto(chat_id=update.effective_user.id,
                      photo='https://robohash.org/{0}?set=set4&bgset=bg{1}&size=500x500'.format(username, result_id),
                      caption=_('Here\'s your cute little {0}!').format(username.capitalize()), timeout=60)

    elif 'monster' in query:
        user_data.setdefault('monster', list())
        username = query.split('monster')[1].strip()
        user_data['monster'].append(username)
        result_id = update.chosen_inline_result.result_id
        bot.send_chat_action(chat_id=update.effective_user.id, action=ChatAction.UPLOAD_PHOTO)
        bot.edit_message_text(
            text=_('Your monster has been summoned successfully! Go and pet it! Create more using /create'),
            chat_id=user_data['config']['create_chat_id'], message_id=user_data['config']['create_message_id'])
        bot.sendPhoto(chat_id=update.effective_user.id,
                      photo='https://robohash.org/{0}?set=set2&bgset=bg{1}&size=500x500'.format(username, result_id),
                      caption=_('Here\'s your {0}! Don\'t worry he\'s friendly.').format(username.capitalize()), timeout=60)

    elif 'username' in query:
        user_data.setdefault('cute', list())
        username = query.split('username')[1].strip()
        user_data['cute'].append(username)
        result_id = update.chosen_inline_result.result_id
        bot.send_chat_action(chat_id=update.effective_user.id, action=ChatAction.UPLOAD_PHOTO)
        bot.edit_message_text(
            text=_('Your cute creature has been summoned successfully! Go and pet it! Create more using /create'),
            chat_id=user_data['config']['create_chat_id'], message_id=user_data['config']['create_message_id'])
        bot.sendPhoto(chat_id=update.effective_user.id, photo='http://api.adorable.io/avatars/{0}'.format(username),
                      caption=_('Here\'s your little {0}!').format(username.capitalize(), timeout=60))


def register(dp):
    dp.add_handler(ChosenInlineResultHandler(chosen_inline_manager, pass_user_data=True, pass_job_queue=True))

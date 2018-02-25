from localization import gettext_from_update
import time


def feedback_msg(bot, job):
    _ = gettext_from_update(job.context)
    bot.send_message(chat_id=job.context.effective_user.id, text=_("Thanks for availing the services that I provide! 😃 Take a look at names of avatars you have created till now using /list.\n\nShare how you feel about my services with my creator, leave a feedback and rate me using /rate."))
    print("Job executed at {0}".format(time.time()))  # TODO: Remove this print statement when you're done testing things out!

import gettext
from localization.available import available_locales
import config

text = {}
for locale in available_locales:
    cat = gettext.Catalog("text", localedir="locale", languages=[locale])
    text[locale] = cat.gettext

default = text[config.default_language]


def gettext_from_update(update):
    language_code = update.effective_user.language_code
    if language_code:
        return text.get(language_code[:2], default)
    else:
        return default

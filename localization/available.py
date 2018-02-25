# -*- coding: utf-8 -*-
"""Defines a dict of all available locales to the language name"""
from pprint import pprint

OFFSET = 127462 - ord('A')


def flag(code):
    return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)


available_locales = {
    'en': ' English (US)',
    'de': ' Deutsch (DE)',
    'ru': ' Русский',
    'it': ' Italian',
    # 'nl': flag('NL') + ' Nederlands (NL)',
    # 'ar': flag('SA') + ' العربيه'
    # 'fa': flag('IR') + ' فارسی',
    'es': flag('ES') + ' Español (ES)',
    # 'id': flag('ID') + ' Bahasa Indonesia',
    # 'pt': flag('BR') + ' Português Brasileiro',

}

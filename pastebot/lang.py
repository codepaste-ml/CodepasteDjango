# coding=utf-8
import random

TRANSLATION = {
    'start_message': 'Send any text to create paste',
    'list': '🗒 Список',
    'settings': '⚙ Настройки',

    'paste_message': '{}',
    'raw_paste_message': '{}\n{}',

    'settings_text': '⚙ Настройки\n'
                     '\n'
                     'Вывод `raw` ссылок:  {}',

    'enabled': '✅ Включено',
    'disabled': '♦ Выключено',
    'back': '⬅ Назад',

    'print_raw': 'Вывод raw ссылок',

    'paste_list': 'Список ваших записей: \n{}',

    'something_went_wrong': 'Что-то пошло не так 😕\nПопробуйте повторить позже. \nЕсли проблема повторится, '
                            'свяжитесь с @DarkKeks',

    'started': '✅ Бот перезапущен',
    'bot_is_restarting': '⚙ Перезапускаемся',
    'not_enough_permissions': '🚫 Недостаточно прав',
}


def translate(key):
    if key in TRANSLATION:
        if isinstance(TRANSLATION[key], list):
            return random.choice(TRANSLATION[key])
        return TRANSLATION[key]
    else:
        return key

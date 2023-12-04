from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

startup_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Создать профиль')]
],
resize_keyboard=True,
input_field_placeholder='find me.'
)

gender_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Я девушка'), KeyboardButton(text='Я парень')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

search_gender_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Девушек'), KeyboardButton(text='Парней'), KeyboardButton(text='Все равно')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

end_state = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Завершить')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🔥'), KeyboardButton(text='👤')]
    ],
    resize_keyboard=True,
    input_field_placeholder='find me'
)

menu_msg_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🔥'), KeyboardButton(text='👤'), KeyboardButton(text='❣️')]
    ],
    resize_keyboard=True,
    input_field_placeholder='find me'
)

settings_profile = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='1'), KeyboardButton(text='2'), KeyboardButton(text='3'), KeyboardButton(text='🔥')]
    ],
    resize_keyboard=True,
    input_field_placeholder='find me'
)

looking_profiles = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='❤️'), KeyboardButton(text='💌 | 📹'), KeyboardButton(text='👎'), KeyboardButton(text='💤')]
    ],
    resize_keyboard=True,
    input_field_placeholder='find me'
)


reaction_liked_profiles = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='❤️'), KeyboardButton(text='👎'), KeyboardButton(text='🔙')]
    ],
    resize_keyboard=True,
    input_field_placeholder='find me'
)

love_msg = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отмена')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
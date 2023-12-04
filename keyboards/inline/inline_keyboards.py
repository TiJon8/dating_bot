from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

startup_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать профиль', callback_data='create_profil')]
])


yearBD_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1970', callback_data='yearBD_1970')]
])


sex_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Девушка', callback_data='female'), InlineKeyboardButton(text='Парень', callback_data='male')]
    ]
)

search_gender_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Девушек', callback_data='find_female'), InlineKeyboardButton(text='Парней', callback_data='find_male'), InlineKeyboardButton(text='Всех', callback_data='find_any')]
    ]
)


mouths = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

mouthBD_keyboard = InlineKeyboardBuilder()
for mouth in mouths:
    call_mouth = ''
    if mouth == 'Январь':
        call_mouth = 'january'
    mouthBD_keyboard.button(text=f"{mouth}", callback_data=f"mouthBD_{call_mouth}")
mouthBD_keyboard.adjust(3)
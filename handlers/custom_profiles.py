from loader import dp

from aiogram.types import (CallbackQuery, Message)
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.default.default_keyboards import gender_keyboard, search_gender_keyboard, end_state, menu_keyboard
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from utils.db.db_api import db_API

class MainState(StatesGroup):
    main = State()

class UserStateProfil(StatesGroup):
    gender = State()


class CustopProfile(StatesGroup):
    customID = State()
    username = State()
    gender = State()
    prefer_gender = State()
    name = State()
    age = State()
    city = State()
    desc = State()
    media = State()


async def convert_ph(photo):
    photo_id = photo.file_id
    photo_unique_id = photo.file_unique_id
    photo_width = photo.width
    photo_height = photo.height
    photo_size = photo.file_size

    return ['photo', {'photo_id': photo_id, 'photo_unique_id': photo_unique_id, 'photo_width': photo_width, 'photo_height': photo_height, 'photo_size': photo_size}]

async def convert_vd(video):
    video_id = video.file_id
    video_unique_id = video.file_unique_id
    video_width = video.width
    video_height = video.height
    video_duration = video.duration
    video_name = video.file_name
    video_mime_type = video.mime_type
    video_size = video.file_size

    return ['video', {'video_id': video_id, 'video_unique_id': video_unique_id, 'video_width': video_width, 'video_height': video_height, 'video_duration': video_duration, 'video_name': video_name, 'video_mime_type': video_mime_type, 'video_size': video_size}]


@dp.message(MainState.main, F.text == 'Создать')
async def create_custom_profile(message: Message, state: FSMContext):
    await message.answer('Введи id')
    await state.set_state(CustopProfile.customID)


@dp.message(CustopProfile.customID)
async def custom_profile_id(message: Message, state: FSMContext):
    await state.update_data(id = message.text)
    await message.answer('Введи username')
    await state.set_state(CustopProfile.username)



@dp.message(CustopProfile.username)
async def custom_profile_username(message: Message, state: FSMContext):
    await state.update_data(username = message.text)
    await message.answer('Давай знакомиться. Кто ты?', reply_markup=gender_keyboard)
    await state.set_state(CustopProfile.gender)


@dp.message(CustopProfile.gender)
async def process_state_gender(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if message.text == 'Я девушка':
        await state.update_data(gender = 'girl')
        await db_API.add_girl_profile(data["id"], data["username"], 'girl')
    elif message.text == 'Я парень':
        await state.update_data(gender = 'boy')
        await db_API.add_boy_profile(data["id"], data["username"], 'boy')

    await message.answer('Кого ищешь?', reply_markup=search_gender_keyboard)
    await state.set_state(CustopProfile.prefer_gender)


@dp.message(CustopProfile.prefer_gender)
async def custom_profile_search_gender(message: Message, state: FSMContext) -> None:
    if message.text == 'Девушек':
        await state.update_data(prefer_gender = 'girls')
    elif message.text == 'Парней':
        await state.update_data(prefer_gender = 'boys')
    else:
        await state.update_data(prefer_gender = 'any')

    await message.answer('Как тебя называть?', reply_markup=ReplyKeyboardRemove())
    await state.set_state(CustopProfile.name)


@dp.message(CustopProfile.name)
async def custom_profile_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name = message.text)
    await message.answer('Сколько тебе лет?')
    await state.set_state(CustopProfile.age)


@dp.message(CustopProfile.age)
async def custom_profile_age(message: Message, state: FSMContext) -> None:
    await state.update_data(age = message.text)
    await message.answer('Укажи свой город')
    await state.set_state(CustopProfile.city)


@dp.message(CustopProfile.city)
async def custom_profile_city(message: Message, state: FSMContext) -> None:
    await state.update_data(city = message.text)
    await message.answer('Напиши пару слов о себе')
    await state.set_state(CustopProfile.desc)


@dp.message(CustopProfile.desc)
async def custom_profile_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description = message.text)
    await message.answer('Напоследок загрузи минимум одну фотографию или видео для профиля (максимум 10 файлов)')
    await state.set_state(CustopProfile.media)


@dp.message(CustopProfile.media, F.photo)
async def process_state_photo(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    us = await db_API.get_user(data["id"])
    media = us['media']
    if media:
        media_len = len(media)
    else: 
        media_len = 0
    if media_len >= 10:
        await test_def(message=message, state=state)
        return
    else:
        photo = message.photo[-1]
        document = await convert_ph(photo)

        if data['gender'] == 'girl':
            await db_API.update_girl_media(data["id"], doc=document)
        elif data['gender'] == 'boy':
            await db_API.update_boy_media(data["id"], doc=document)
        media_len += 1
    await message.answer('Хорошее фото, можешь загрузить еще или завершить', reply_markup=end_state)


@dp.message(CustopProfile.media, F.text == 'Завершить')
async def process_state_clear(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if data['gender'] == 'girl':
        await db_API.update_girl_profile(data["id"], data['prefer_gender'], data['name'], data['age'], data['city'], data['description'])
    elif data['gender'] == 'boy':
        await db_API.update_boy_profile(data["id"], data['prefer_gender'], data['name'], data['age'], data['city'], data['description'])
    await state.set_state(MainState.main)
    await message.answer('Проифль создан')
    await message.answer('🔥 — смотреть анкеты\n👤 — мой профиль', reply_markup=menu_keyboard)


async def test_def(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if data['gender'] == 'girl':
        await db_API.update_girl_profile(data["id"], data['prefer_gender'], data['name'], data['age'], data['city'], data['description'])
    elif data['gender'] == 'boy':
        await db_API.update_boy_profile(data["id"], data['prefer_gender'], data['name'], data['age'], data['city'], data['description'])
    await state.set_state(MainState.main)
    await message.answer('Проифль создан')
    await message.answer('🔥 — смотреть анкеты\n👤 — мой профиль', reply_markup=menu_keyboard)
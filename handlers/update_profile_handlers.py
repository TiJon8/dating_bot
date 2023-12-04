from loader import dp

from aiogram.types import (Message)
from aiogram import F
from aiogram.fsm.context import FSMContext
from keyboards.default.default_keyboards import gender_keyboard, search_gender_keyboard, end_state
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from .default_handlers import show_profile
from typing import List
from utils.db.db_api import db_API


from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

from states.states import(MainState, ChangeProfile, UserStateProfil)
from utils.assistiants import (convert_ph, convert_vd)





@dp.message(MainState.main, F.text == '1')
async def change_media_profile(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if data["gender"] == 'girl':
        await db_API.clear_girl_media(message.from_user.id)
    elif data["gender"] == 'boy':
        await db_API.clear_boy_media(message.from_user.id)

    await message.answer(f'Пришли медифайлы, уже загруженные будут заменены', reply_markup=ReplyKeyboardRemove())
    await state.set_state(ChangeProfile.media)


@dp.message(MainState.main, F.text == '2')
async def change_bio_profile(message: Message, state: FSMContext) -> None:
    await message.answer(f'Кого ищешь?', reply_markup=search_gender_keyboard)
    await state.set_state(ChangeProfile.search_gender)


@dp.message(MainState.main, F.text == '3')
async def set_profile_again(message: Message, state: FSMContext) -> None:
    await message.answer('Давай знакомиться. Кто ты?', reply_markup=gender_keyboard)
    await state.set_state(ChangeProfile.again_profile)


@dp.message(ChangeProfile.again_profile)
async def again_profile_gender(message: Message, state: FSMContext) -> None:
    if message.text == 'Я девушка':
        await state.update_data(gender = 'girl')
        await db_API.again_girl_profile(message.from_user.id, message.from_user.username, 'girl')
    elif message.text == 'Я парень':
        await state.update_data(gender = 'boy')
        await db_API.again_boy_profile(message.from_user.id, message.from_user.username, 'boy')
    else:
        await message.answer('Укажи пол')
        return

    await message.answer('Кого ищешь?', reply_markup=search_gender_keyboard)
    await state.set_state(UserStateProfil.search_gender)


@dp.message(ChangeProfile.search_gender)
async def update_search_gender_profile(message: Message, state: FSMContext):
    if message.text == 'Девушек':
        await state.update_data(prefer_gender = 'girls')
    elif message.text == 'Парней':
        await state.update_data(prefer_gender = 'boys')
    elif message.text == 'Все равно':
        await state.update_data(prefer_gender = 'any')
    else:
        await message.answer('Укажи кого ищешь')
        return

    data = await state.get_data()
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=f'{data["name"]}')]], resize_keyboard=True)
    await message.answer('Как тебя называть?', reply_markup=kb)
    await state.set_state(ChangeProfile.name)


@dp.message(ChangeProfile.name)
async def update_name_profile(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    data = await state.get_data()
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=f'{data["age"]}')]
    ], resize_keyboard=True)
    await message.answer('Сколько тебе лет?', reply_markup=kb)
    await state.set_state(ChangeProfile.age)


@dp.message(ChangeProfile.age)
async def update_age_profile(message: Message, state: FSMContext):
    await state.update_data(age = message.text)
    data = await state.get_data()
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=f'{data["city"]}')]
    ], resize_keyboard=True)
    await message.answer('Укажи город', reply_markup=kb)
    await state.set_state(ChangeProfile.city)

@dp.message(ChangeProfile.city)
async def update_city_profile(message: Message, state: FSMContext):
    await state.update_data(city = message.text)
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Оставить текущее')]
    ], resize_keyboard=True)
    await message.answer('Напиши пару слов о себе', reply_markup=kb)
    await state.set_state(ChangeProfile.desc)


@dp.message(ChangeProfile.desc)
async def update_description_profile(message: Message, state: FSMContext):
    if message.text == 'Оставить текущее':
        pass
    else:
        await state.update_data(description = message.text)
    
    data = await state.get_data() 
    if data["gender"] == 'girl':
        await db_API.update_girl_profile(message.from_user.id, data["prefer_gender"], data["name"], data["age"], data["city"], data["description"])
    elif data["gender"] == 'boy':
        await db_API.update_boy_profile(message.from_user.id, data["prefer_gender"], data["name"], data["age"], data["city"], data["description"])
    await process_state_clear(message=message, state=state)



@dp.message(ChangeProfile.media, F.media_group_id)
async def process_state_album(message: Message, state: FSMContext, album: List) -> None:
    data = await state.get_data()
    us = await db_API.get_user(message.from_user.id)
    media = us['media']
    if media:
        media_len = len(media)
    else: 
        media_len = 0
    for i in album:
        if i[0] == 'photo' and i[1]:
            if media_len >= 10:
                await process_state_clear(message=message, state=state)
                return
            else:
                for photo in i[1]:
                    document = await convert_ph(photo)

                    if data['gender'] == 'girl':
                        await db_API.update_girl_media(message.from_user.id, doc=document)
                    elif data['gender'] == 'boy':
                        await db_API.update_boy_media(message.from_user.id, doc=document)
                    media_len += 1
        elif i[0] == 'video' and i[1]:
            if media_len >= 10:
                await process_state_clear(message=message, state=state)
                return
            else:
                for video in i[1]:
                    document = await convert_vd(video)

                    if data['gender'] == 'girl':
                        await db_API.update_girl_media(message.from_user.id, doc=document)
                    elif data['gender'] == 'boy':
                        await db_API.update_boy_media(message.from_user.id, doc=document)
                    media_len += 1

    await message.answer(f'Готово, можешь добавить еще или завершить', reply_markup=end_state)



@dp.message(ChangeProfile.media, F.photo)
async def process_state_photo(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    us = await db_API.get_user(message.from_user.id)
    media = us['media']
    if media:
        media_len = len(media)
    else: 
        media_len = 0

    if media_len >= 10:
        await process_state_clear(message=message, state=state)
        return
    else:
        photo = message.photo[-1]
        document = await convert_ph(photo)

        if data['gender'] == 'girl':
            await db_API.update_girl_media(message.from_user.id, doc=document)
        elif data['gender'] == 'boy':
            await db_API.update_boy_media(message.from_user.id, doc=document)
        media_len += 1

    await message.answer(f'Хорошее фото, можешь добавить еще или завершить', reply_markup=end_state)



@dp.message(ChangeProfile.media, F.video)
async def process_state_video(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    us = await db_API.get_user(message.from_user.id)
    media = us['media']
    if media:
        media_len = len(media)
    else: 
        media_len = 0

    if media_len >= 10:
        await process_state_clear(message=message, state=state)
        return
    else:
        video = message.video
        document = await convert_vd(video)

        if data['gender'] == 'girl':
            await db_API.update_girl_media(message.from_user.id, doc=document)
        elif data['gender'] == 'boy':
            await db_API.update_boy_media(message.from_user.id, doc=document)
        media_len += 1

    await message.answer(f'Отличное видео, можешь добавить еще или завершить', reply_markup=end_state)


@dp.message(ChangeProfile.media, F.text == 'Завершить')
async def process_state_clear(message: Message, state: FSMContext) -> None:
    us = await db_API.get_user(message.from_user.id)
    await state.set_state(MainState.main)
    await state.set_data(us)
    await message.answer('Проифль обновлен')
    await show_profile(message=message, state=state)
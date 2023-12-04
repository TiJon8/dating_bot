from loader import dp

from aiogram.types import (CallbackQuery, Message)
from aiogram import F
from aiogram.fsm.context import FSMContext
from keyboards.default.default_keyboards import gender_keyboard, search_gender_keyboard, end_state, menu_keyboard
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from typing import List
from utils.db.db_api import db_API


from states.states import (MainState, UserStateProfil)
from utils.assistiants import (convert_vd, convert_ph)


@dp.callback_query(F.data == 'create_profil')
async def create_profil(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer('Давай знакомиться. Кто ты?', reply_markup=gender_keyboard)
    await callback.answer()
    await state.set_state(UserStateProfil.gender)


@dp.message(UserStateProfil.gender)
async def process_state_gender(message: Message, state: FSMContext) -> None:
    if message.text == 'Я девушка':
        await state.update_data(gender = 'girl')
        await db_API.add_girl_profile(message.from_user.id, message.from_user.username, message.from_user.first_name, 'girl')
    elif message.text == 'Я парень':
        await state.update_data(gender = 'boy')
        await db_API.add_boy_profile(message.from_user.id, message.from_user.username, message.from_user.first_name, 'boy')
    else:
        await message.answer('Укажи пол')
        return

    await message.answer('Кого ищешь?', reply_markup=search_gender_keyboard)
    await state.set_state(UserStateProfil.search_gender)


@dp.message(UserStateProfil.search_gender)
async def process_state_search_gender(message: Message, state: FSMContext) -> None:
    if message.text == 'Девушек':
        await state.update_data(prefer_gender = 'girls')
    elif message.text == 'Парней':
        await state.update_data(prefer_gender = 'boys')
    elif message.text == 'Все равно':
        await state.update_data(prefer_gender = 'any')
    else:
        await message.answer('Укажи кого ищешь')
        return

    await message.answer('Как тебя называть?', reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserStateProfil.name)


@dp.message(UserStateProfil.name)
async def process_state_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name = message.text)
    await message.answer('Сколько тебе лет?')
    await state.set_state(UserStateProfil.age)


@dp.message(UserStateProfil.age)
async def process_state_age(message: Message, state: FSMContext) -> None:
    await state.update_data(age = message.text)
    await message.answer('Укажи свой город')
    await state.set_state(UserStateProfil.city)


@dp.message(UserStateProfil.city)
async def process_state_city(message: Message, state: FSMContext) -> None:
    await state.update_data(city = message.text)
    await message.answer('Напиши пару слов о себе')
    await state.set_state(UserStateProfil.desc)


@dp.message(UserStateProfil.desc)
async def process_state_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description = message.text)
    await message.answer('Напоследок загрузи минимум одну фотографию или видео для профиля (максимум 10 файлов)')
    await state.set_state(UserStateProfil.media)


@dp.message(UserStateProfil.media, F.media_group_id)
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
            for photo in i[1]:
                if media_len >= 10:
                    await process_state_clear(message=message, state=state)
                    return
                else:
                    document = await convert_ph(photo)
                    if data['gender'] == 'girl':
                        await db_API.update_girl_media(message.from_user.id, doc=document)
                    elif data['gender'] == 'boy':
                        await db_API.update_boy_media(message.from_user.id, doc=document)
                    media_len += 1
        elif i[0] == 'video' and i[1]:
            for video in i[1]:
                if media_len >= 10:
                    await process_state_clear(message=message, state=state)
                    return
                else:
                    document = await convert_vd(video)
                    if data['gender'] == 'girl':
                        await db_API.update_girl_media(message.from_user.id, doc=document)
                    elif data['gender'] == 'boy':
                        await db_API.update_boy_media(message.from_user.id, doc=document)
                    media_len += 1
    await message.answer('Хорошо, твоя анкета готова, можешь загрузить еще или завершить', reply_markup=end_state)



@dp.message(UserStateProfil.media, F.photo)
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
    await message.answer('Хорошее фото, можешь загрузить еще или завершить', reply_markup=end_state)


@dp.message(UserStateProfil.media, F.video)
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
    await message.answer('Отличное видео, можешь загрузить еще или завершить', reply_markup=end_state)


@dp.message(UserStateProfil.media, F.text == 'Завершить')
async def process_state_clear(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    if data['gender'] == 'girl':
        await db_API.update_girl_profile(message.from_user.id, data['prefer_gender'], data['name'], data['age'], data['city'], data['description'])
    elif data['gender'] == 'boy':
        await db_API.update_boy_profile(message.from_user.id, data['prefer_gender'], data['name'], data['age'], data['city'], data['description'])

    await message.answer('Все готово, теперь ты можешь смотреть анкеты других')
    user = await db_API.get_user(message.from_user.id)
    await state.set_state(MainState.main)
    await state.set_data(user)

    await message.answer('🔥 — смотреть анкеты\n👤 — мой профиль', reply_markup=menu_keyboard)


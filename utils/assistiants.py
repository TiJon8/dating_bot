from loader import bot
from aiogram.utils.media_group import MediaGroupBuilder
from keyboards.default.default_keyboards import (
    menu_keyboard, menu_msg_keyboard)
from states.states import (MainState)
from utils.db.db_api import db_API


# функция отображения главного меню
async def back_to_main(message, state):
    user = await state.get_data()
    await state.set_state(MainState.main)
    if len(user['like_me']) > 0:
        await message.answer('🔥 — смотреть анкеты\n👤 — мой профиль\n❣️ — сообщения для меня', reply_markup=menu_msg_keyboard)
    else:
        await message.answer('🔥 — смотреть анкеты\n👤 — мой профиль', reply_markup=menu_keyboard)


# показать профиль лайкнувшего
async def show_liked_me(user_id, user, action):
    name = user['name']
    age = user['age']
    city = user['city']
    desc = user['description']

    if action == '❤️':
        media_group = MediaGroupBuilder(caption=f"Ты понравился:\n\n{name}, {age}, {city} — {desc}")
    elif type(action) == dict:
        media_group = MediaGroupBuilder(caption=f"📹 Тебе отправили кружок:\n\n{name}, {age}, {city} — {desc}")
    else:
        media_group = MediaGroupBuilder(caption=f"💌 Для тебя сообщение: {action}\n\n{name}, {age}, {city} — {desc}")

    media = user['media']
    for cont in media:
        if cont[0] == 'photo':
            photo_obj = cont[1]
            photo_id = photo_obj['photo_id']
            media_group.add_photo(media=photo_id)
        elif cont[0] == 'video':
            video_obj = cont[1]
            video_id = video_obj['video_id']
            media_group.add_video(media=video_id)
            
    await bot.send_media_group(user_id, media=media_group.build())


# собрать профиль
async def convert_media_group(user_id, user) -> None:
    name = user['name']
    age = user['age']
    city = user['city']
    desc = user['description']
    media_group = MediaGroupBuilder(caption=f"{name}, {age}, {city} — {desc}")

    media = user['media']
    for cont in media:
        if cont[0] == 'photo':
            photo_obj = cont[1]
            photo_id = photo_obj['photo_id']
            media_group.add_photo(media=photo_id)
        elif cont[0] == 'video':
            video_obj = cont[1]
            video_id = video_obj['video_id']
            media_group.add_video(media=video_id)
            
    await bot.send_media_group(user_id, media=media_group.build())


# получить просмотренные профили
async def get_viewed(data: list) -> list:
    viewed = []
    for ids in data:
        usid = int(ids['_id'])
        viewed.append(usid)
    return viewed


# получить профили из бд
async def get_profiles(message, data):
    if data.get('viewed'):
        viewed = await get_viewed(data=data['viewed'])
    else:
        viewed = None

    if data["prefer_gender"] == 'girls':
        return await db_API.get_girls_profiles(user_id=message.from_user.id, viewed=viewed)
    if data["prefer_gender"] == 'boys':
        return await db_API.get_boys_profiles(user_id=message.from_user.id, viewed=viewed)
    if data["prefer_gender"] == 'any':
        return await db_API.get_any_profiles(user_id=message.from_user.id, viewed=viewed)


# показать следующий профиль
async def show_next_profile(message, state, data, documents):
    try:
        user = documents[0]
        await convert_media_group(message.from_user.id, user=user)
        await state.update_data(viewing=documents)
    except IndexError:
        cursor = await get_profiles(message=message, data=data)
        documents = await cursor.to_list(length=1)
        if documents:
            new_user = documents[0]
            await convert_media_group(message.from_user.id, user=new_user)
            await state.update_data(viewing=documents)
        else:
            await state.update_data(viewing=documents)
            await message.answer('Похоже анкеты закончились', reply_markup=menu_keyboard)
            await state.set_state(MainState.main)


# получить новые профили из бд
async def get_new_profiles(message, state, data):
    if data.get('viewed'):
        cursor = await get_profiles(message=message, data=data)
        new_documents = await cursor.to_list(length=1)
        try:
            new_user = new_documents[0]
            await convert_media_group(message.from_user.id, user=new_user)
            await state.update_data(viewing=new_documents)
        except IndexError:
            await message.answer('Похоже анкеты закончились', reply_markup=menu_keyboard)
            await state.set_state(MainState.main)
    else:
        cursor = await get_profiles(message=message, data=data)
        new_documents = await cursor.to_list(length=1)
        try:
            new_user = new_documents[0]
            await convert_media_group(message.from_user.id, user=new_user)
            await state.update_data(viewing=new_documents)
            await state.update_data(viewed=[])
        except IndexError:
            await message.answer('Похоже анкеты закончились', reply_markup=menu_keyboard)
            await state.set_state(MainState.main)


# возвращает список с полученным фото
async def convert_ph(photo) -> list:
    photo_id = photo.file_id
    photo_unique_id = photo.file_unique_id
    photo_width = photo.width
    photo_height = photo.height
    photo_size = photo.file_size

    return ['photo', {'photo_id': photo_id, 'photo_unique_id': photo_unique_id, 'photo_width': photo_width, 'photo_height': photo_height, 'photo_size': photo_size}]


# возвращает список с полученным видео
async def convert_vd(video) -> list:
    video_id = video.file_id
    video_unique_id = video.file_unique_id
    video_width = video.width
    video_height = video.height
    video_duration = video.duration
    video_name = video.file_name
    video_mime_type = video.mime_type
    video_size = video.file_size

    return ['video', {'video_id': video_id, 'video_unique_id': video_unique_id, 'video_width': video_width, 'video_height': video_height, 'video_duration': video_duration, 'video_name': video_name, 'video_mime_type': video_mime_type, 'video_size': video_size}]
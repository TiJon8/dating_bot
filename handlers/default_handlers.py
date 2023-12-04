from loader import bot, dp

from keyboards.default.default_keyboards import (
    settings_profile, reaction_liked_profiles)
from keyboards.inline.inline_keyboards import (
    startup_keyboard)

from aiogram import F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from utils.db.db_api import db_API
from utils.assistiants import (back_to_main, show_liked_me)
from states.states import (MainState, LookLiked)

from utils.types import Album
from aiogram.utils.media_group import MediaGroupBuilder






@dp.message(CommandStart())
async def startup_message(message: Message, state: FSMContext):
    # user = await db_API.get_user(message.from_user.id)
    user = await state.get_data()
    await message.answer('Find Me - найди того, кто действительно тебе нужен')
    if user:
        await state.set_data(user)
        await state.set_state(MainState.main)
        await back_to_main(message=message, state=state)
    else:
        await message.answer('Прежде чем смотреть анкеты, создай свой профиль', reply_markup=startup_keyboard)


@dp.message(MainState.main, F.text == '❣️')
async def show_liked_profile(message: Message, state: FSMContext):
    await state.set_state(LookLiked.look_)

    data = await state.get_data()
    liked_user = data['like_me'][0]
    user = await db_API.get_user(int(liked_user['_id']))
    action = liked_user['action']
    await message.answer('✨👀', reply_markup=reaction_liked_profiles)
    await show_liked_me(message.from_user.id, user, action)
    if type(action) == dict:
        print(action)
        await bot.send_video_note(message.from_user.id, f'{action["note_id"]}')


@dp.message(LookLiked.look_, F.text == '❤️')
async def like_too_profile(message: Message, state: FSMContext):
    data = await state.get_data()

    liked_list = data['like_me']
    liked_user = liked_list[0]
    await message.answer(f'Это взаимно, начинай общаться 👉 @{liked_user["username"]}')
    if data.get('viewed'):
        viewed_profiles = data['viewed']
        viewed_profiles.append(liked_user)
        await state.update_data(viewed=viewed_profiles)
    else:
        viewed = []
        viewed.append(liked_user)
        await state.update_data(viewed=viewed)

    liked_list.pop(0)
    await state.update_data(like_me=liked_list)
    
    try:
        new_liked_user = liked_list[0]
        user = await db_API.get_user(int(new_liked_user['_id']))
        action = new_liked_user['action']
        await show_liked_me(message.from_user.id, user, action)
        if type(action) == dict:
            print(action)
            await bot.send_video_note(message.from_user.id, f'{action["note_id"]}')
    except IndexError:
        await message.answer('На этом пока все')
        await back_to_main(message=message, state=state)



@dp.message(LookLiked.look_, F.text == '👎')
async def dislike_too_profile(message: Message, state: FSMContext):
    data = await state.get_data()

    liked_list = data['like_me']
    dislike_user = liked_list[0]
    if data.get('viewed'):
        viewed_profiles = data['viewed']
        viewed_profiles.append(dislike_user)
        await state.update_data(viewed=viewed_profiles)
    else:
        viewed = []
        viewed.append(dislike_user)
        await state.update_data(viewed=viewed)

    liked_list.pop(0)
    await state.update_data(like_me=liked_list)

    try:
        new_liked_user = liked_list[0]
        user = await db_API.get_user(int(new_liked_user['_id']))
        action = new_liked_user['action']
        await show_liked_me(message.from_user.id, user, action)
        if type(action) == dict:
            await bot.send_video_note(message.from_user.id, f'{action["note_id"]}')
    except IndexError:
        await message.answer('На этом пока все')
        await back_to_main(message=message, state=state)



@dp.message(LookLiked.look_, F.text == '🔙')
async def back_main(message: Message, state: FSMContext):
    await back_to_main(message=message, state=state)


@dp.message(MainState.main, F.text == '👤')
async def show_profile(message: Message, state: FSMContext):
    user = await state.get_data()
    print(user)

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
    
    await bot.send_media_group(message.from_user.id, media=media_group.build())
    await message.answer('1 — изменить фото/видео\n2 — изменить данные о себе\n3 — заполнить анкету заново\n🔥 — смотреть анкеты', reply_markup=settings_profile)





# @dp.message(MainState.main or F.text or F.photo or F.video or F.media_group_id)
# async def another_message(message: Message):
#     await message.answer('Не понял тебя', reply_markup=menu_keyboard)
from loader import bot, dp
from aiogram import F
from aiogram.types import (Message, CallbackQuery)
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from utils.db.db_api import db_API
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.media_group import MediaGroupBuilder
from keyboards.default.default_keyboards import (
    menu_keyboard, looking_profiles, love_msg)
from utils.assistiants import (back_to_main, convert_media_group, get_new_profiles, show_next_profile)
from states.states import (MainState, LookingProfiles)



@dp.message(MainState.main, F.text == '🔥')
async def find_profiles(message: Message, state: FSMContext):
    await message.answer('✨🔍', reply_markup=looking_profiles)
    await state.set_state(LookingProfiles.next_)
    data = await state.get_data()
    if data.get('viewing'):
        documents = data['viewing']
        if documents[0]:
            user = documents[0]
            await convert_media_group(message.from_user.id, user=user)
    else:
        await get_new_profiles(message=message, state=state, data=data)
    



@dp.message(LookingProfiles.next_, F.text == '❤️')
async def find_next_profile(message: Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    
    documents = data['viewing']
    like = documents[0]
    if len(data['like_me']) >= 1:
        liked = data['like_me']
        liked_user = liked[0]
        if liked_user['_id'] == like['_id']:
            await message.answer(f'Это взаимно, начинай общаться 👉 @{liked_user["username"]}')
            liked.pop(0)
            await state.update_data(like_me=liked)
    print(like)
    viewed_data = data['viewed']
    viewed_data.append(like)
    await state.update_data(viewed=viewed_data)
    await db_API.set_like(message.from_user.id, message.from_user.username, message.from_user.first_name, like['_id'], data['gender'], like['gender'], '❤️')
    documents.pop(0)

    await show_next_profile(message=message, state=state, data=data, documents=documents)


@dp.message(LookingProfiles.next_, F.text == '👎')
async def find_next_dis_profile(message: Message, state: FSMContext):
    data = await state.get_data()
    print(data)

    documents = data['viewing']
    dislike = documents[0]
    if len(data['like_me']) >= 1:
        liked = data['like_me']
        liked_user = liked[0]
        if liked_user['_id'] == dislike['_id']:
            liked.pop(0)
            await state.update_data(like_me=liked)
    print(dislike)
    viewed_data = data['viewed']
    viewed_data.append(dislike)
    await state.update_data(viewed=viewed_data)
    documents.pop(0)

    await show_next_profile(message=message, state=state, data=data, documents=documents)


@dp.message(LookingProfiles.next_, F.text == '💌 | 📹')
async def love_msg_profile(message: Message, state: FSMContext):
    await message.answer('Напиши сообщение или отправь видеопослание', reply_markup=love_msg)
    await state.set_state(LookingProfiles.love_msg_)


@dp.message(LookingProfiles.love_msg_, F.text == 'Отмена')
async def cancel_lovemsg_profile(message: Message, state: FSMContext):
    data = await state.get_data()
    documents = data['viewing']
    user = documents[0]
    await message.answer('✨🔍', reply_markup=looking_profiles)
    await convert_media_group(message.from_user.id, user=user)
    await state.set_state(LookingProfiles.next_)



@dp.message(LookingProfiles.love_msg_, F.video_note)
async def send_love_video(message: Message, state: FSMContext):
    vd_note = message.video_note
    doc = {
        'note_id': vd_note.file_id,
        'note_unique_id': vd_note.file_unique_id,
        'note_lenght': vd_note.length,
        'note_duration': vd_note.duration,
        'note_size': vd_note.file_size
    }
    data = await state.get_data()

    documents = data['viewing']
    note_msg = documents[0]
    if len(data['like_me']) >= 1:
        liked = data['like_me']
        liked_user = liked[0]
        if liked_user['_id'] == note_msg['_id']:
            await message.answer(f'Это взаимно, начинай общаться 👉 @{liked_user["username"]}')
            liked.pop(0)
            await state.update_data(like_me=liked)
    print(note_msg)
    viewed_data = data['viewed']
    viewed_data.append(note_msg)
    await state.update_data(viewed=viewed_data)
    await db_API.set_like(message.from_user.id, message.from_user.username, message.from_user.first_name, note_msg['_id'], data['gender'], note_msg['gender'], doc)
    documents.pop(0)

    await message.answer('Сообщение отправлено', reply_markup=looking_profiles)
    await state.set_state(LookingProfiles.next_)

    await show_next_profile(message=message, state=state, data=data, documents=documents)



@dp.message(LookingProfiles.love_msg_)
async def send_love_msg(message: Message, state: FSMContext):
    if message.photo or message.video:
        await message.answer('Можно отправить только сообщение или видео кружок')
        return
    
    data = await state.get_data()

    msg_text = message.text
    documents = data['viewing']
    msg = documents[0]
    if len(data['like_me']) >= 1:
        liked = data['like_me']
        liked_user = liked[0]
        if liked_user['_id'] == msg['_id']:
            await message.answer(f'Это взаимно, начинай общаться 👉 @{liked_user["username"]}')
            liked.pop(0)
            await state.update_data(like_me=liked)
    print(msg)
    viewed_data = data['viewed']
    viewed_data.append(msg)
    await state.update_data(viewed=viewed_data)
    await db_API.set_like(message.from_user.id, message.from_user.username, message.from_user.first_name, msg['_id'], data['gender'], msg['gender'], msg_text)
    documents.pop(0)

    await message.answer('Сообщение отправлено', reply_markup=looking_profiles)
    await state.set_state(LookingProfiles.next_)

    await show_next_profile(message=message, state=state, data=data, documents=documents)





@dp.message(LookingProfiles.next_, F.text == '💤')
async def find_next_dis_profile(message: Message, state: FSMContext):
    await message.answer('Подождем пока тебе кто-то напишет', reply_markup=menu_keyboard)
    await back_to_main(message=message, state=state)
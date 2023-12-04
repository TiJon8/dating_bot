from aiogram.fsm.state import State, StatesGroup

class MainState(StatesGroup):
    main = State()

class LookLiked(StatesGroup):
    look_ = State()

class UserStateProfil(StatesGroup):
    gender = State()
    search_gender = State()
    name = State()
    age = State()
    city = State()
    desc = State()
    media = State()

class LookingProfiles(StatesGroup):
    next_ = State()
    love_msg_ = State()

class ChangeProfile(StatesGroup):
    search_gender = State()
    name = State()
    age = State()
    city = State()
    desc = State()
    media = State()
    again_profile = State()
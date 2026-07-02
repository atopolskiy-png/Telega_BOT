from aiogram.fsm.state import State, StatesGroup


# ==========================================
# Регистрация игрока
# ==========================================

class RegisterPlayer(StatesGroup):

    waiting_for_name = State()


# ==========================================
# Создание нового опроса
# ==========================================

class CreatePoll(StatesGroup):

    waiting_for_date = State()

    waiting_for_time = State()

    waiting_for_place = State()


# ==========================================
# Ответ игрока
# ==========================================

class PlayerAnswer(StatesGroup):

    waiting_for_attendance = State()

    waiting_for_payment = State()
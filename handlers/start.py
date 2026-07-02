from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from keyboards import admin_menu
from states import RegisterPlayer
from database import player_exists, add_player

router = Router()


# =====================================================
# /start
# =====================================================

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):

    user_id = message.from_user.id

    # =========================
    # АДМИН
    # =========================
    if user_id == ADMIN_ID:

        await message.answer(
            "🏒 Панель администратора",
            reply_markup=admin_menu
        )
        return

    # =========================
    # УЖЕ ЕСТЬ ИГРОК
    # =========================
    if player_exists(user_id):

        await message.answer(
            "🏒 С возвращением!"
        )
        return

    # =========================
    # РЕГИСТРАЦИЯ
    # =========================
    await message.answer(
        "🏒 Добро пожаловать в Golden Hawks!\n\n"
        "Введите ваше имя и фамилию."
    )

    await state.set_state(RegisterPlayer.waiting_for_name)


# =====================================================
# РЕГИСТРАЦИЯ ИГРОКА
# =====================================================

@router.message(RegisterPlayer.waiting_for_name)
async def register_player(message: Message, state: FSMContext):

    name = message.text.strip()

    if len(name) < 3:
        await message.answer("❌ Введите корректное имя.")
        return

    add_player(message.from_user.id, name)

    await state.clear()

    await message.answer(
        f"✅ {name}, регистрация завершена!\n\n"
        "Теперь ты в системе 🏒"
    )
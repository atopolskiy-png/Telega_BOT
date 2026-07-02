from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from database import (
    create_poll,
    get_poll,
    get_all_players,
    get_answers,
    save_attendance,
    save_payment,
    get_player
)

from keyboards import (
    attendance_keyboard,
    payment_keyboard,
    send_poll_keyboard,
    report_keyboard
)

from states import CreatePoll

router = Router()


# =====================================================
# 📢 НОВЫЙ ОПРОС
# =====================================================

@router.message(F.text == "📢 Новый опрос")
async def new_poll(message: Message, state: FSMContext):

    if message.from_user.id != ADMIN_ID:
        return

    await state.clear()
    await message.answer("Введите дату тренировки:")
    await state.set_state(CreatePoll.waiting_for_date)


# =====================================================
# 📅 ДАТА
# =====================================================

@router.message(CreatePoll.waiting_for_date)
async def poll_date(message: Message, state: FSMContext):

    await state.update_data(date=message.text)

    await message.answer("Введите время тренировки:")
    await state.set_state(CreatePoll.waiting_for_time)


# =====================================================
# 🕒 ВРЕМЯ
# =====================================================

@router.message(CreatePoll.waiting_for_time)
async def poll_time(message: Message, state: FSMContext):

    await state.update_data(time=message.text)

    await message.answer("Введите место тренировки:")
    await state.set_state(CreatePoll.waiting_for_place)


# =====================================================
# 📍 МЕСТО + СОЗДАНИЕ
# =====================================================

@router.message(CreatePoll.waiting_for_place)
async def poll_place(message: Message, state: FSMContext):

    data = await state.get_data()

    create_poll(
        date=data.get("date"),
        time=data.get("time"),
        place=message.text
    )

    await state.clear()

    await message.answer(
        f"""🏒 Опрос создан!

📅 {data.get('date')}
🕒 {data.get('time')}
📍 {message.text}
""",
        reply_markup=send_poll_keyboard
    )


# =====================================================
# 📢 ОТПРАВКА ОПРОСА
# =====================================================

@router.callback_query(F.data == "send_poll")
async def send_poll(callback: CallbackQuery):

    await callback.answer()

    poll = get_poll()
    players = get_all_players()

    if not poll:
        await callback.message.answer("❌ Нет активного опроса")
        return

    text = (
        "🏒 Golden Hawks\n\n"
        f"📅 {poll.get('date')}\n"
        f"🕒 {poll.get('time')}\n"
        f"📍 {poll.get('place')}\n\n"
        "Вы придёте на тренировку?"
    )

    for uid in players.keys():
        try:
            await callback.bot.send_message(
                int(uid),
                text,
                reply_markup=attendance_keyboard
            )
        except Exception as e:
            print("SEND ERROR:", uid, e)

    await callback.message.edit_text("✅ Опрос отправлен!")


# =====================================================
# 🏒 ПРИДУ / НЕ ПРИДУ
# =====================================================

@router.callback_query(F.data == "attendance_yes")
async def attendance_yes(callback: CallbackQuery):

    await callback.answer()
    save_attendance(callback.from_user.id, True)

    await callback.message.answer("💰 Абонемент оплачен?")
    await callback.message.answer("👇", reply_markup=payment_keyboard)


@router.callback_query(F.data == "attendance_no")
async def attendance_no(callback: CallbackQuery):

    await callback.answer()
    save_attendance(callback.from_user.id, False)

    await callback.message.answer("💰 Абонемент оплачен?")
    await callback.message.answer("👇", reply_markup=payment_keyboard)


# =====================================================
# 💰 ОПЛАТА
# =====================================================

@router.callback_query(F.data == "payment_yes")
async def payment_yes(callback: CallbackQuery):

    await callback.answer()
    save_payment(callback.from_user.id, True)

    await callback.message.answer("✅ Спасибо за ответ!")


@router.callback_query(F.data == "payment_no")
async def payment_no(callback: CallbackQuery):

    await callback.answer()
    save_payment(callback.from_user.id, False)

    await callback.message.answer("❌ Спасибо за ответ!")


# =====================================================
# 📋 ОТЧЕТ
# =====================================================

@router.message(F.text == "📋 Ответы")
async def show_report(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    answers = get_answers()

    if not answers:
        await message.answer("Пока нет ответов")
        return

    text = "🏒 ОТЧЕТ\n\n"

    for user_id, data in answers.items():

        player = get_player(user_id)
        name = player["name"] if player else user_id

        text += (
            f"👤 {name}\n"
            f"🏒 {'Придет' if data.get('attendance') else 'Не придет'}\n"
            f"💰 {'Оплатил' if data.get('payment') else 'Не оплатил'}\n\n"
        )

    await message.answer(text, reply_markup=report_keyboard)


# =====================================================
# 🔄 ОБНОВИТЬ ОТЧЕТ
# =====================================================

@router.callback_query(F.data == "refresh_report")
async def refresh_report(callback: CallbackQuery):

    await callback.answer()

    answers = get_answers()

    text = "🏒 ОТЧЕТ\n\n"

    for user_id, data in answers.items():

        player = get_player(user_id)
        name = player["name"] if player else user_id

        text += (
            f"👤 {name}\n"
            f"🏒 {'Придет' if data.get('attendance') else 'Не придет'}\n"
            f"💰 {'Оплатил' if data.get('payment') else 'Не оплатил'}\n\n"
        )

    await callback.message.edit_text(text, reply_markup=report_keyboard)


# =====================================================
# 👥 ИГРОКИ
# =====================================================

@router.message(F.text == "👥 Игроки")
async def show_players(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    players = get_all_players()

    text = "👥 Игроки команды:\n\n"

    for user_id, player in players.items():
        text += f"👤 {player.get('name')}\n"

    await message.answer(text)


# =====================================================
# 📨 НАПОМИНАНИЕ (ИСПРАВЛЕНО)
# =====================================================

@router.message(F.text == "📨 Напомнить")
async def remind(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    players = get_all_players() or {}

    poll = get_poll()

    if not poll:
        await message.answer("❌ Нет активного опроса")
        return

    text = (
        "🏒 Напоминание о тренировке!\n\n"
        f"📅 {poll.get('date')}\n"
        f"🕒 {poll.get('time')}\n"
        f"📍 {poll.get('place')}\n\n"
        "Пожалуйста, ответьте на опрос 🙏"
    )

    sent = 0

    for user_id in players.keys():

        try:
            await message.bot.send_message(
                int(user_id),
                text
            )
            sent += 1

        except Exception as e:
            print("SEND ERROR:", user_id, e)

    await message.answer(f"📨 Напоминание отправлено: {sent} игрокам")
# =====================================================
# ❌ ОТМЕНА
# =====================================================

@router.callback_query(F.data == "cancel_poll")
async def cancel_poll(callback: CallbackQuery):

    await callback.answer()
    await callback.message.edit_text("❌ Опрос отменён")


# =====================================================
# 📨 INLINE НАПОМИНАНИЕ
# =====================================================

@router.callback_query(F.data == "remind_players")
async def remind_players(callback: CallbackQuery):

    await callback.answer()

    answers = get_answers()
    players = get_all_players()

    for user_id in players.keys():

        if str(user_id) in answers:
            continue

        try:
            await callback.bot.send_message(
                int(user_id),
                "🏒 Напоминание: ответьте на опрос!"
            )
        except:
            continue

    await callback.message.answer("📨 Напоминания отправлены!")
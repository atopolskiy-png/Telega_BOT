from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# =====================================================
# МЕНЮ АДМИНИСТРАТОРА
# =====================================================

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📢 Новый опрос")
        ],
        [
            KeyboardButton(text="📋 Ответы")
        ],
        [
            KeyboardButton(text="👥 Игроки")
        ],
        [
            KeyboardButton(text="📨 Напомнить")
        ]
    ],
    resize_keyboard=True
)

# =====================================================
# КНОПКИ ОПРОСА
# =====================================================

attendance_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Приду",
                callback_data="attendance_yes"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Не приду",
                callback_data="attendance_no"
            )
        ]
    ]
)

# =====================================================
# ОПЛАТА
# =====================================================

payment_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💰 Оплатил",
                callback_data="payment_yes"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Не оплатил",
                callback_data="payment_no"
            )
        ]
    ]
)

# =====================================================
# ПОДТВЕРЖДЕНИЕ РАССЫЛКИ
# =====================================================

send_poll_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📢 Отправить опрос",
                callback_data="send_poll"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Отмена",
                callback_data="cancel_poll"
            )
        ]
    ]
)

# =====================================================
# ОТЧЕТ
# =====================================================

report_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔄 Обновить",
                callback_data="refresh_report"
            )
        ],
        [
            InlineKeyboardButton(
                text="📨 Напомнить",
                callback_data="remind_players"
            )
        ]
    ]
)
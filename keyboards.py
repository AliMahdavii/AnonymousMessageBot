from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard():
    keyboard = InlineKeyboardMarkup()

    link_button = InlineKeyboardButton(
        "🔗 لینک اختصاصی من",
        callback_data="my_link"
    )

    messages_button = InlineKeyboardButton(
        "📥 پیام‌های دریافتی",
        callback_data="my_messages"
    )

    keyboard.add(link_button)
    keyboard.add(messages_button)

    return keyboard


def reply_keyboard(message_id):
    keyboard = InlineKeyboardMarkup()

    reply_button = InlineKeyboardButton(
        "💬 Reply",
        callback_data=f"reply:{message_id}"
    )

    keyboard.add(reply_button)

    return keyboard


def language_keyboard():
    keyboard = InlineKeyboardMarkup()

    persian_button = InlineKeyboardButton(
        "🇮🇷 فارسی",
        callback_data="language:fa"
    )

    english_button = InlineKeyboardButton(
        "🇬🇧 English",
        callback_data="language:en"
    )

    keyboard.add(
        persian_button,
        english_button
    )

    return keyboard

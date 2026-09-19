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

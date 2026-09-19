from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard():
    keyboard = InlineKeyboardMarkup()

    link_button = InlineKeyboardButton(
        "🔗 لینک اختصاصی من",
        callback_data="my_link"
    )

    keyboard.add(link_button)

    return keyboard


def reply_keyboard(message_id):
    keyboard = InlineKeyboardMarkup()

    reply_button = InlineKeyboardButton(
        "💬 Reply",
        callback_data=f"reply:{message_id}"
    )

    keyboard.add(reply_button)

    return keyboard
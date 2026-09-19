from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard():
    keyboard = InlineKeyboardMarkup()

    send_button = InlineKeyboardButton(
        "✉️ ارسال پیام",
        callback_data="send_message"
    )

    link_button = InlineKeyboardButton(
        "🔗 لینک اختصاصی من",
        callback_data="my_link"
    )

    keyboard.add(send_button)
    keyboard.add(link_button)

    return keyboard

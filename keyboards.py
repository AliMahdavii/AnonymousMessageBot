from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard():
    keyboard = InlineKeyboardMarkup()

    send_button = InlineKeyboardButton(
        "✉️ ارسال پیام",
        callback_data="send_message"
    )

    keyboard.add(send_button)

    return keyboard

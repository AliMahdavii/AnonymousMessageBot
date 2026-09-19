import telebot

from config import BOT_TOKEN
from keyboards import main_keyboard
from database import create_table, save_message


bot = telebot.TeleBot(BOT_TOKEN)

waiting_users = set()

create_table()


@bot.message_handler(commands=["start"])
def start(message):
    text = (
        "👋 سلام!\n\n"
        "اینجا می‌تونی پیامت رو برای صاحب این بات ارسال کنی.\n\n"
        "پیامت رو بنویس و ارسال کن 👇"
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=main_keyboard()
    )


@bot.callback_query_handler(func=lambda call: call.data == "send_message")
def send_message_callback(call):
    bot.answer_callback_query(call.id)

    waiting_users.add(call.from_user.id)

    bot.send_message(
        call.message.chat.id,
        "✍️ پیامت رو بنویس و همینجا ارسال کن."
    )


@bot.message_handler(content_types=["text"])
def receive_message(message):
    user_id = message.from_user.id

    if user_id not in waiting_users:
        return

    waiting_users.remove(user_id)

    username = message.from_user.username
    first_name = message.from_user.first_name
    text = message.text

    save_message(
        sender_id=user_id,
        username=username,
        first_name=first_name,
        message=text
    )

    print("----- NEW MESSAGE -----")
    print("User ID:", user_id)
    print("Username:", message.from_user.username)
    print("First name:", message.from_user.first_name)
    print("Message:", message.text)
    print("-----------------------")

    bot.send_message(
        message.chat.id,
        "✅ پیامت با موفقیت دریافت شد."
    )


print("Bot is running...")

bot.infinity_polling()

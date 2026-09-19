import telebot

from config import BOT_TOKEN
from keyboards import main_keyboard
from database import create_table, save_message


bot = telebot.TeleBot(BOT_TOKEN)

waiting_users = {}

create_table()


@bot.message_handler(commands=["start"])
def start(message):
    parts = message.text.split(maxsplit=1)

    if len(parts) > 1:
        receiver_id = int(parts[1])

        waiting_users[message.from_user.id] = receiver_id

        bot.send_message(
            message.chat.id,
            "👋 سلام!\n\n"
            "اینجا می‌تونی پیامت رو برای صاحب این بات ارسال کنی.\n\n"
            "پیامت رو بنویس و ارسال کن 👇"
        )

        return

    text = (
        "👋 سلام خوبی!\n\n"
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

    waiting_users[call.from_user.id] = call.from_user.id

    bot.send_message(
        call.message.chat.id,
        "✍️ پیامت رو بنویس و همینجا ارسال کن."
    )


@bot.callback_query_handler(func=lambda call: call.data == "my_link")
def my_link_callback(call):
    bot.answer_callback_query(call.id)

    bot_info = bot.get_me()

    link = f"https://t.me/{bot_info.username}?start={call.from_user.id}"

    bot.send_message(
        call.message.chat.id,
        "🔗 لینک اختصاصی دریافت پیام شما:\n\n"
        f"{link}\n\n"
        "این لینک را برای دیگران ارسال کنید تا بتوانند برای شما پیام بفرستند."
    )


@bot.message_handler(content_types=["text"])
def receive_message(message):
    sender_id = message.from_user.id

    if sender_id not in waiting_users:
        return

    receiver_id = waiting_users.pop(sender_id)

    username = message.from_user.username
    first_name = message.from_user.first_name
    text = message.text

    save_message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        username=username,
        first_name=first_name,
        message=text
    )

    receiver_text = (
        "📩 پیام جدید\n\n"
        "💬 پیام:\n"
        f"{text}"
    )

    bot.send_message(
        receiver_id,
        receiver_text 
    )

    print("----- NEW MESSAGE -----")
    print("Sender ID:", sender_id)
    print("Receiver ID:", receiver_id)
    print("Username:", username)
    print("First name:", first_name)
    print("Message:", text)
    print("-----------------------")

    bot.send_message(
        message.chat.id,
        "✅ پیامت با موفقیت دریافت شد."
    )


print("Bot is running...")

bot.infinity_polling()

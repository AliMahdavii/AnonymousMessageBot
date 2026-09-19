import telebot

from config import BOT_TOKEN
from database import create_table, save_message, get_message
from keyboards import main_keyboard, reply_keyboard


bot = telebot.TeleBot(BOT_TOKEN)


waiting_users = {}
waiting_for_reply = {}


create_table()


@bot.message_handler(commands=["start"])
def start(message):
    parts = message.text.split(maxsplit=1)

    # User opened someone's personal link
    if len(parts) > 1:
        try:
            receiver_id = int(parts[1])
        except ValueError:
            bot.send_message(
                message.chat.id,
                "❌ لینک نامعتبر است."
            )
            return

        waiting_users[message.from_user.id] = receiver_id

        bot.send_message(
            message.chat.id,
            "👋 سلام!\n\n"
            "اینجا می‌تونی یک پیام ناشناس ارسال کنی.\n\n"
            "🔒 هویتت برای گیرنده نمایش داده نمی‌شود.\n\n"
            "✍️ پیامت رو بنویس و ارسال کن 👇"
        )

        return

    # Normal /start
    text = (
        "👋 سلام!\n\n"
        "به پیام ناشناس خوش اومدی.\n\n"
        "🔒 می‌تونی لینک اختصاصی خودت رو دریافت کنی "
        "تا دیگران برات پیام ناشناس بفرستن."
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=main_keyboard()
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
        "این لینک را برای دیگران ارسال کنید تا بتوانند "
        "برای شما پیام ناشناس بفرستند."
    )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("reply:")
)
def reply_callback(call):
    bot.answer_callback_query(call.id)

    try:
        message_id = int(call.data.split(":")[1])
    except (ValueError, IndexError):
        bot.send_message(
            call.message.chat.id,
            "❌ پیام نامعتبر است."
        )
        return

    result = get_message(message_id)

    if not result:
        bot.send_message(
            call.message.chat.id,
            "❌ این پیام دیگر در دسترس نیست."
        )
        return

    sender_id, receiver_id = result

    # Only the receiver can reply
    if call.from_user.id != receiver_id:
        bot.send_message(
            call.message.chat.id,
            "❌ این پیام برای شما نیست."
        )
        return

    waiting_for_reply[call.from_user.id] = message_id

    bot.send_message(
        call.message.chat.id,
        "✍️ پاسخ خودت رو بنویس."
    )


@bot.message_handler(content_types=["text"])
def receive_message(message):
    user_id = message.from_user.id

    # -------------------------
    # Anonymous reply
    # -------------------------

    if user_id in waiting_for_reply:
        message_id = waiting_for_reply.pop(user_id)

        result = get_message(message_id)

        if not result:
            bot.send_message(
                message.chat.id,
                "❌ این پیام دیگر در دسترس نیست."
            )
            return

        sender_id, receiver_id = result

        bot.send_message(
            sender_id,
            "💬 پاسخ جدید:\n\n"
            f"{message.text}"
        )

        bot.send_message(
            message.chat.id,
            "✅ پاسخ ارسال شد."
        )

        return

    # -------------------------
    # New anonymous message
    # -------------------------

    sender_id = user_id

    if sender_id not in waiting_users:
        return

    receiver_id = waiting_users.pop(sender_id)

    username = message.from_user.username
    first_name = message.from_user.first_name
    text = message.text

    message_id = save_message(
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
        receiver_text,
        reply_markup=reply_keyboard(message_id)
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

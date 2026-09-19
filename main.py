import telebot

from config import BOT_TOKEN
from database import (
    create_table,
    save_message,
    get_message,
    get_received_messages,
    save_waiting_user,
    get_waiting_user,
    delete_waiting_user,
    save_waiting_reply,
    get_waiting_reply,
    delete_waiting_reply
)
from keyboards import (
    main_keyboard,
    reply_keyboard,
    language_keyboard
)
from telebot.types import BotCommand, MenuButtonCommands


bot = telebot.TeleBot(BOT_TOKEN)


def setup_bot_menu():
    commands = [
        BotCommand("start", "شروع کار با بات"),
        BotCommand("language", "تغییر زبان"),
        BotCommand("my_link", "لینک اختصاصی من"),
        BotCommand("my_messages", "پیام‌های دریافتی")
    ]

    bot.set_my_commands(commands)

    bot.set_chat_menu_button(
        menu_button=MenuButtonCommands()
    )


create_table()
setup_bot_menu()


# =========================
# START
# =========================

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

        save_waiting_user(
            message.from_user.id,
            receiver_id
        )

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


# =========================
# LANGUAGE
# =========================

@bot.message_handler(commands=["language"])
def language_command(message):
    bot.send_message(
        message.chat.id,
        "🌐 زبان را انتخاب کن:",
        reply_markup=language_keyboard()
    )


# =========================
# MY LINK
# =========================

@bot.callback_query_handler(
    func=lambda call: call.data == "my_link"
)
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


@bot.message_handler(commands=["my_link"])
def my_link_command(message):
    bot_info = bot.get_me()

    link = f"https://t.me/{bot_info.username}?start={message.from_user.id}"

    bot.send_message(
        message.chat.id,
        "🔗 لینک اختصاصی دریافت پیام شما:\n\n"
        f"{link}\n\n"
        "این لینک را برای دیگران ارسال کنید تا بتوانند "
        "برای شما پیام ناشناس بفرستند."
    )


# =========================
# MY MESSAGES
# =========================

@bot.callback_query_handler(
    func=lambda call: call.data == "my_messages"
)
def my_messages_callback(call):
    bot.answer_callback_query(call.id)

    receiver_id = call.from_user.id

    messages = get_received_messages(receiver_id)

    if not messages:
        bot.send_message(
            call.message.chat.id,
            "📭 هنوز هیچ پیام ناشناسی دریافت نکردی."
        )
        return

    for message_id, text, created_at in messages:
        message_text = (
            "📩 پیام ناشناس\n\n"
            f"💬 {text}\n\n"
            f"🕐 {created_at}"
        )

        bot.send_message(
            call.message.chat.id,
            message_text,
            reply_markup=reply_keyboard(message_id)
        )


@bot.message_handler(commands=["my_messages"])
def my_messages_command(message):
    receiver_id = message.from_user.id

    messages = get_received_messages(receiver_id)

    if not messages:
        bot.send_message(
            message.chat.id,
            "📭 هنوز هیچ پیام ناشناسی دریافت نکردی."
        )
        return

    for message_id, text, created_at in messages:
        message_text = (
            "📩 پیام ناشناس\n\n"
            f"💬 {text}\n\n"
            f"🕐 {created_at}"
        )

        bot.send_message(
            message.chat.id,
            message_text,
            reply_markup=reply_keyboard(message_id)
        )


# =========================
# REPLY
# =========================

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

    save_waiting_reply(
        call.from_user.id,
        message_id
    )

    bot.send_message(
        call.message.chat.id,
        "✍️ پاسخ خودت رو بنویس."
    )


# =========================
# RECEIVE TEXT MESSAGE
# =========================

@bot.message_handler(content_types=["text"])
def receive_message(message):
    user_id = message.from_user.id

    # -------------------------
    # Anonymous reply
    # -------------------------

    message_id = get_waiting_reply(user_id)

    if message_id:
        delete_waiting_reply(user_id)

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

    receiver_id = get_waiting_user(sender_id)

    if receiver_id is None:
        return

    delete_waiting_user(sender_id)

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

    # Console logging
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


# =========================
# RUN BOT
# =========================

print("Bot is running...")

bot.infinity_polling()

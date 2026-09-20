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
    delete_waiting_reply,
    save_user_language,
    get_user_language
)
from keyboards import (
    main_keyboard,
    reply_keyboard,
    language_keyboard
)
from telebot.types import BotCommand, MenuButtonCommands
from translations import get_text


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
            language = get_user_language(message.from_user.id)

            bot.send_message(
                message.chat.id,
                get_text(
                    language,
                    "invalid_link"
                )
            )
            return

        save_waiting_user(
            message.from_user.id,
            receiver_id
        )

        language = get_user_language(message.from_user.id)

        bot.send_message(
            message.chat.id,
            get_text(
                language,
                "anonymous_message_prompt"
            )
        )

        return

    # Normal /start
    language = get_user_language(message.from_user.id)

    text = get_text(
        language,
        "welcome"
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=main_keyboard(language)
    )


# =========================
# LANGUAGE
# =========================

@bot.message_handler(commands=["language"])
def language_command(message):
    language = get_user_language(message.from_user.id)

    bot.send_message(
        message.chat.id,
        get_text(language, "language_select"),
        reply_markup=language_keyboard()
    )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("language:")
)
def language_callback(call):
    language = call.data.split(":")[1]

    if language not in ("fa", "en"):
        bot.answer_callback_query(
            call.id,
            "❌ Invalid language."
        )
        return

    save_user_language(
        call.from_user.id,
        language
    )

    bot.answer_callback_query(call.id)

    bot.send_message(
        call.message.chat.id,
        get_text(language, "language_changed")
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

    language = get_user_language(call.from_user.id)

    bot.send_message(
        call.message.chat.id,
        get_text(
            language,
            "my_link",
            link=link
        )
    )


@bot.message_handler(commands=["my_link"])
def my_link_command(message):
    bot_info = bot.get_me()

    link = f"https://t.me/{bot_info.username}?start={message.from_user.id}"

    language = get_user_language(message.from_user.id)

    bot.send_message(
        message.chat.id,
        get_text(
            language,
            "my_link",
            link=link
        )
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

    receiver_language = get_user_language(receiver_id)

    if not messages:
        bot.send_message(
            call.message.chat.id,
            get_text(
                receiver_language,
                "no_messages"
            )
        )
        return

    for message_id, text, created_at in messages:
        message_text = get_text(
            receiver_language,
            "anonymous_message",
            text=text,
            created_at=created_at
        )

        bot.send_message(
            call.message.chat.id,
            message_text,
            reply_markup=reply_keyboard(message_id, receiver_language)
        )


@bot.message_handler(commands=["my_messages"])
def my_messages_command(message):
    receiver_id = message.from_user.id

    messages = get_received_messages(receiver_id)

    if not messages:
        language = get_user_language(message.from_user.id)

        bot.send_message(
            message.chat.id,
            get_text(
                language,
                "no_messages"
            )
        )
        return

    language = get_user_language(receiver_id)

    for message_id, text, created_at in messages:
        message_text = get_text(
            language,
            "anonymous_message",
            text=text,
            created_at=created_at
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
        language = get_user_language(call.from_user.id)

        bot.send_message(
            call.message.chat.id,
            get_text(language, "invalid_message")
        )
        return

    result = get_message(message_id)

    if not result:
        language = get_user_language(call.from_user.id)

        bot.send_message(
            call.message.chat.id,
            get_text(language, "message_not_available")
        )
        return

    sender_id, receiver_id = result

    # Only the receiver can reply
    if call.from_user.id != receiver_id:
        language = get_user_language(call.from_user.id)

        bot.send_message(
            call.message.chat.id,
            get_text(language, "not_your_message")
        )
        return

    save_waiting_reply(
        call.from_user.id,
        message_id
    )

    language = get_user_language(call.from_user.id)

    bot.send_message(
        call.message.chat.id,
        get_text(language, "reply_prompt")
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
            language = get_user_language(message.from_user.id)

            bot.send_message(
                message.chat.id,
                get_text(
                    language,
                    "message_not_available"
                )
            )

            return

        sender_id, receiver_id = result

        sender_language = get_user_language(sender_id)
        receiver_language = get_user_language(receiver_id)

        bot.send_message(
            sender_id,
            get_text(
                sender_language,
                "new_reply",
                text=message.text
            )
        )

        bot.send_message(
            message.chat.id,
            get_text(
                receiver_language,
                "reply_sent"
            )
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

    receiver_language = get_user_language(receiver_id)

    receiver_text = get_text(
        receiver_language,
        "new_message",
        text=text
    )

    bot.send_message(
        receiver_id,
        receiver_text,
        reply_markup=reply_keyboard(message_id, receiver_language)
    )

    # Console logging
    print("----- NEW MESSAGE -----")
    print("Sender ID:", sender_id)
    print("Receiver ID:", receiver_id)
    print("Username:", username)
    print("First name:", first_name)
    print("Message:", text)
    print("-----------------------")

    sender_language = get_user_language(sender_id)

    bot.send_message(
        message.chat.id,
        get_text(
            sender_language,
            "message_sent"
        )
    )


# =========================
# RUN BOT
# =========================

print("Bot is running...")

bot.infinity_polling()

import telebot

from config import BOT_TOKEN
from keyboards import main_keyboard


bot = telebot.TeleBot(BOT_TOKEN)


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

    bot.send_message(
        call.message.chat.id,
        "✍️ پیامت رو بنویس و همینجا ارسال کن."
    )


print("Bot is running...")

bot.infinity_polling()

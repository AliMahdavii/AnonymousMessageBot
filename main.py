import telebot

from config import BOT_TOKEN


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "سلام 👋\n"
        "به بات پیام ناشناس خوش اومدی."
    )


print("Bot is running...")

bot.infinity_polling()

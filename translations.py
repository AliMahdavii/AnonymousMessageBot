TEXTS = {
    "fa": {
        "invalid_link": "❌ لینک نامعتبر است.",

        "anonymous_message_prompt": (
            "👋 سلام!\n\n"
            "اینجا می‌تونی یک پیام ناشناس ارسال کنی.\n\n"
            "🔒 هویتت برای گیرنده نمایش داده نمی‌شود.\n\n"
            "✍️ پیامت رو بنویس و ارسال کن 👇"
        ),

        "welcome": (
            "👋 سلام!\n\n"
            "به پیام ناشناس خوش اومدی.\n\n"
            "🔒 می‌تونی لینک اختصاصی خودت رو دریافت کنی "
            "تا دیگران برات پیام ناشناس بفرستن."
        ),

        "language_select": "🌐 زبان را انتخاب کن:",

        "language_changed": "🇮🇷 زبان با موفقیت به فارسی تغییر کرد.",

        "my_link": (
            "🔗 لینک اختصاصی دریافت پیام شما:\n\n"
            "{link}\n\n"
            "این لینک را برای دیگران ارسال کنید تا بتوانند "
            "برای شما پیام ناشناس بفرستند."
        ),

        "no_messages": "📭 هنوز هیچ پیام ناشناسی دریافت نکردی.",

        "anonymous_message": (
            "📩 پیام ناشناس\n\n"
            "💬 {text}\n\n"
            "🕐 {created_at}"
        ),

        "invalid_message": "❌ پیام نامعتبر است.",

        "message_not_available": "❌ این پیام دیگر در دسترس نیست.",

        "not_your_message": "❌ این پیام برای شما نیست.",

        "reply_prompt": "✍️ پاسخ خودت رو بنویس.",

        "new_reply": (
            "💬 پاسخ جدید:\n\n"
            "{text}"
        ),

        "reply_sent": "✅ پاسخ ارسال شد.",

        "message_sent": "✅ پیامت با موفقیت دریافت شد.",

        "new_message": (
            "📩 پیام جدید\n\n"
            "💬 پیام:\n"
            "{text}"
        ),
    },

    "en": {
        "invalid_link": "❌ Invalid link.",

        "anonymous_message_prompt": (
            "👋 Hello!\n\n"
            "You can send an anonymous message here.\n\n"
            "🔒 Your identity will not be shown to the recipient.\n\n"
            "✍️ Write your message and send it 👇"
        ),

        "welcome": (
            "👋 Hello!\n\n"
            "Welcome to Anonymous Message.\n\n"
            "🔒 Get your personal link and share it "
            "with others to receive anonymous messages."
        ),

        "language_select": "🌐 Choose your language:",

        "language_changed": "🇬🇧 Language changed to English.",

        "my_link": (
            "🔗 Your personal message link:\n\n"
            "{link}\n\n"
            "Share this link with others so they can "
            "send you anonymous messages."
        ),

        "no_messages": "📭 You haven't received any anonymous messages yet.",

        "anonymous_message": (
            "📩 Anonymous message\n\n"
            "💬 {text}\n\n"
            "🕐 {created_at}"
        ),

        "invalid_message": "❌ Invalid message.",

        "message_not_available": "❌ This message is no longer available.",

        "not_your_message": "❌ This message does not belong to you.",

        "reply_prompt": "✍️ Write your reply.",

        "new_reply": (
            "💬 New reply:\n\n"
            "{text}"
        ),

        "reply_sent": "✅ Reply sent.",

        "message_sent": "✅ Your message was received successfully.",

        "new_message": (
            "📩 New message\n\n"
            "💬 Message:\n"
            "{text}"
        ),
    }
}


def get_text(language, key, **kwargs):
    language = language if language in TEXTS else "fa"

    text = TEXTS[language].get(key)

    if text is None:
        text = TEXTS["fa"].get(key, key)

    return text.format(**kwargs)

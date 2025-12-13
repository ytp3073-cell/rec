import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8419880200:AAGMgJ2_q6iMqVtAwii3N4rTmbzNNUluNIg"
API_URL = "https://reaction.xo.je/reaction.php"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Reaction Bot Ready!\n\n"
        "Use:\n"
        "/react <telegram_post_link>\n\n"
        "Example:\n"
        "/react https://t.me/BLNK_SOUL/56"
    )

# /react
async def react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ Post link missing\n\n"
            "Use:\n"
            "/react https://t.me/channel/123"
        )
        return

    post_link = context.args[0]

    try:
        r = requests.get(API_URL, params={"post": post_link}, timeout=10)
        data = r.json()["results"]

        msg = (
            "✅ *Reaction Report*\n\n"
            f"📌 Post: {data['target_post']}\n"
            f"🎯 Summary: {data['summary']}\n"
            f"😄 Emojis: {' '.join(data['emojis_used'])}\n"
            f"👁 Views Added: {data['views_increased']}\n"
            f"⏱ Time: {data['total_time']}\n\n"
            f"👨‍💻 Developer: {data['👨‍💻 Developer']}\n"
            f"📣 Channel: {data['📣 Channel']}"
        )

        await update.message.reply_text(msg, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text("⚠️ API Error or Server Down")

# main
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("react", react))

print("Bot running...")
app.run_polling()

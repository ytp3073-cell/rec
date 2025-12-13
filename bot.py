import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8419880200:AAGMgJ2_q6iMqVtAwii3N4rTmbzNNUluNIg"
API_URL = "https://reaction.xo.je/reaction.php"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Reaction Bot Ready\n\n"
        "Use command:\n"
        "/react <post_link>\n\n"
        "Example:\n"
        "/react https://t.me/BLNK_SOUL/56"
    )

async def react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Post link missing")
        return

    post_link = context.args[0]

    try:
        r = requests.get(API_URL, params={"post": post_link}, timeout=15)
        api_json = r.json()
        data = api_json.get("results", {})

        msg = (
            "✅ *Reaction Report*\n\n"
            f"📌 Post:\n{data.get('target_post')}\n\n"
            f"🎯 {data.get('summary')}\n"
            f"😄 {' '.join(data.get('emojis_used', []))}\n"
            f"👁 Views: {data.get('views_increased')}\n"
            f"⏱ Time: {data.get('total_time')}\n\n"
            f"👨‍💻 Developer: {data.get('👨‍💻 Developer', '@Ban8t')}\n"
            f"📣 Channel: {data.get('📣 Channel')}"
        )

        await update.message.reply_text(msg, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error:\n{e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("react", react))

print("Bot running...")
app.run_polling()

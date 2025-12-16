import logging
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

# ====== SETTINGS ======
TOKEN = "8504393569:AAF2bg-rOQah3-fJPeHP4xizWYLDXlEo5Xg"   # your bot token
ADMIN_ID = 8018964088   # Replace with your Telegram ID
QR_CODE_PATH = "qr.png"  # Save your PhonePe QR image in same folder

UC_PACKS = {
    "500 UC": 300,
    "999 UC": 600,
    "2000 UC": 999,
}

SUPPORT_USERNAME = "@BAN9T"   # replace with your support TG username

# ====== LOGGING ======
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ====== START ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    keyboard = [
        [KeyboardButton("💎 Buy BGMI UC")],
        [KeyboardButton("☎️ Support")]
    ]
    await update.message.reply_text(
        "👋 Welcome! Choose an option:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ====== HANDLE MESSAGE FLOW ======
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "💎 Buy BGMI UC":
        keyboard = [[InlineKeyboardButton(name, callback_data=f"pack_{name}")]
                    for name in UC_PACKS.keys()]
        await update.message.reply_text("💎 Select a UC pack:",
                                        reply_markup=InlineKeyboardMarkup(keyboard))
        return

    elif text == "☎️ Support":
        await update.message.reply_text(f"☎️ Contact support: @{SUPPORT_USERNAME}")
        return

    if context.user_data.get("selected_pack") and "bgmi_id" not in context.user_data:
        if not text.isdigit() or len(text) not in [9, 10]:
            await update.message.reply_text("⚠️ Please enter a valid 9 or 10 digit game ID.")
            return
        context.user_data["bgmi_id"] = text
        await update.message.reply_text("👍 Now send your BGMI Username:")
        return

    if context.user_data.get("bgmi_id") and "bgmi_username" not in context.user_data:
        context.user_data["bgmi_username"] = text
        pack = context.user_data["selected_pack"]

        # Send QR code photo
        await update.message.reply_photo(
            photo=open(QR_CODE_PATH, "rb"),
            caption=(
                f"💳 To complete payment, scan this QR.\n\n"
                f"Amount: ₹{UC_PACKS[pack]}\n\n"
                "📸 Send payment screenshot here after paying."
            )
        )
        return

# ====== UC PACK SELECTION ======
async def uc_pack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pack = query.data.replace("pack_", "")

    context.user_data["selected_pack"] = pack
    await query.message.reply_text(
        f"✅ You selected {pack} for ₹{UC_PACKS[pack]}.\n\n"
        "👉 Please send your BGMI ID now:"
    )

# ====== HANDLE PAYMENT SCREENSHOT ======
async def payment_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        pack = context.user_data.get("selected_pack")
        bgmi_id = context.user_data.get("bgmi_id")
        username = context.user_data.get("bgmi_username")

        if not all([pack, bgmi_id, username]):
            await update.message.reply_text("⚠️ You need to complete the order steps first.")
            return

        caption = (
            f"🆕 New Order\n\n"
            f"👤 User: @{update.message.from_user.username}\n"
            f"🆔 TG ID: {update.message.from_user.id}\n\n"
            f"🎮 BGMI ID: {bgmi_id}\n"
            f"🎮 Username: {username}\n"
            f"💎 Pack: {pack}\n"
            f"💳 Amount: ₹{UC_PACKS[pack]}"
        )

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=file_id,
            caption=caption,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{update.message.from_user.id}_{pack}"),
                 InlineKeyboardButton("❌ Reject", callback_data=f"reject_{update.message.from_user.id}")]
            ])
        )

        await update.message.reply_text("✅ Payment proof sent! Please wait for admin approval.")
        context.user_data.clear()

# ====== ADMIN ACTION ======
async def admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split("_")

    action = data[0]
    user_id = int(data[1])

    if action == "approve":
        pack = data[2]
        await context.bot.send_message(user_id, f"🎉 Your order for {pack} has been approved! UC will be delivered soon.")
        await query.edit_message_caption(query.message.caption + "\n\n✅ Approved")
    elif action == "reject":
        await context.bot.send_message(user_id, f"❌ Your payment was rejected. ☎️ Contact support: @{SUPPORT_USERNAME}")
        await query.edit_message_caption(query.message.caption + "\n\n❌ Rejected")

# ====== MAIN ======
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(uc_pack, pattern="^pack_"))
    app.add_handler(MessageHandler(filters.PHOTO, payment_screenshot))
    app.add_handler(CallbackQueryHandler(admin_action, pattern="^(approve|reject)_"))

    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()

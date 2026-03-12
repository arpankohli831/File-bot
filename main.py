from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = "8760568367:AAE2iBpAr6vlDXe7JyJQtzA6P3GbL0k_Wsc"
BOT_USERNAME = "http://t.me/ARPAN_MODX_FILE_BOT"

ADMINS = [7853887140]

FILES = {}

# ----------------
# START LINK
# ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.args:

        code = context.args[0]

        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url="https://t.me/+yiNqFn6FfZ4wZGM1")],
            [InlineKeyboardButton("✅ Try Again", callback_data=f"file_{code}")]
        ]

        await update.message.reply_text(
            "Send join request then press Try Again.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await update.message.reply_text("Welcome to File Bot")


# ----------------
# ADMIN ADD FILE
# ----------------

async def add_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:
        return

    if update.message.document:

        file = update.message.document

        code = str(len(FILES) + 1)

        FILES[code] = file.file_id

        link = f"http://t.me/ARPAN_MODX_FILE_BOT?start={code}"

        await update.message.reply_text(
            f"✅ File added\n\nDownload link:\n{link}"
        )


# ----------------
# ADMIN DELETE FILE
# ----------------

async def delete_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:
        return

    if len(context.args) == 0:
        await update.message.reply_text("Use: /delete file_number")
        return

    code = context.args[0]

    if code in FILES:

        del FILES[code]

        await update.message.reply_text("✅ File deleted")

    else:

        await update.message.reply_text("File not found")


# ----------------
# TRY AGAIN BUTTON
# ----------------

async def try_again(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    code = query.data.split("_")[1]

    file_id = FILES.get(code)

    if file_id:

        await context.bot.send_document(
            chat_id=query.message.chat.id,
            document=file_id
        )


# ----------------
# MAIN
# ----------------

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CommandHandler("delete", delete_file))

    app.add_handler(MessageHandler(filters.Document.ALL, add_file))

    app.add_handler(CallbackQueryHandler(try_again, pattern="file_"))

    print("Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()
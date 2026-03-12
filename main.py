from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = "8760568367:AAE2iBpAr6vlDXe7JyJQtzA6P3GbL0k_Wsc"
BOT_USERNAME = "http://t.me/ARPAN_MODX_FILE_BOT"
CHANNEL = "@⸙𓊈Ꭺʀᴘᴀɴ MØᗫ✘𓊉ཧོ🦅 BACKUP"

ADMINS = [7853887140]

FILES = {}

# -------------------------
# CHECK CHANNEL JOIN
# -------------------------

async def check_join(user_id, bot):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        if member.status in ["member","administrator","creator"]:
            return True
        return False
    except:
        return False


# -------------------------
# START COMMAND
# -------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if context.args:

        code = context.args[0]

        joined = await check_join(user.id, context.bot)

        if not joined:

            keyboard = [
                [InlineKeyboardButton("📢 Join Channel", url="https://t.me/+FCUf23-QbnMwNmY1")],
                [InlineKeyboardButton("✅ Try Again", callback_data=f"check_{code}")]
            ]

            await update.message.reply_text(
                "❌ Join our channel first then press Try Again.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return

        file_id = FILES.get(code)

        if file_id:

            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file_id
            )
            return

    await update.message.reply_text("Welcome to File Bot!")


# -------------------------
# ADMIN ADD FILE
# -------------------------

async def add_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:
        return

    if update.message.document:

        file = update.message.document

        file_id = file.file_id
        file_name = file.file_name

        code = str(len(FILES) + 1)

        FILES[code] = file_id

        link = f"http://t.me/ARPAN_MODX_FILE_BOT?start={code}"

        await update.message.reply_text(
            f"✅ File Added\n\n{file_name}\n\nDownload Link:\n{link}"
        )


# -------------------------
# ADMIN DELETE FILE
# -------------------------

async def delete_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:
        await update.message.reply_text("❌ Admin only command")
        return

    if len(context.args) == 0:
        await update.message.reply_text("Usage: /delete file_number")
        return

    code = context.args[0]

    if code in FILES:

        del FILES[code]

        await update.message.reply_text("✅ File deleted")

    else:

        await update.message.reply_text("❌ File not found")


# -------------------------
# TRY AGAIN BUTTON
# -------------------------

async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user = query.from_user

    code = query.data.split("_")[1]

    joined = await check_join(user.id, context.bot)

    if not joined:

        await query.answer("❌ Join channel first!", show_alert=True)
        return

    file_id = FILES.get(code)

    if file_id:

        await context.bot.send_document(
            chat_id=query.message.chat.id,
            document=file_id
        )


# -------------------------
# MAIN
# -------------------------

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("delete", delete_file))

    app.add_handler(MessageHandler(filters.Document.ALL, add_file))

    app.add_handler(CallbackQueryHandler(check_button, pattern="check_"))

    print("Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = "YOUR_BOT_TOKEN"
BOT_USERNAME = "http://t.me/ARPAN_MODX_FILE_BOT"
CHANNEL = "@ARPANMODX"

ADMINS = [7853887140]

FILES = {}

# -----------------
# CHECK CHANNEL JOIN
# -----------------

async def check_join(user_id, bot):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        if member.status in ["member","administrator","creator"]:
            return True
        return False
    except:
        return False


# -----------------
# START LINK SYSTEM
# -----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if context.args:

        code = context.args[0]

        joined = await check_join(user.id, context.bot)

        if not joined:

            keyboard = [
                [InlineKeyboardButton("📢 Join Channel", url="https://t.me/+FCUf23-QbnMwNmY1")],
                [InlineKeyboardButton("✅ Try Again", callback_data=f"file_{code}")]
            ]

            await update.message.reply_text(
                "Please join our channel THEN YOU ACCESS ⸙𓊈Ꭺʀᴘᴀɴ MØᗫ✘𓊉ཧོ🦅 FILES",
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

    await update.message.reply_text("WELCOME TO ⸙𓊈Ꭺʀᴘᴀɴ MØᗫ✘𓊉ཧོ🦅 FILE BOT ")


# -----------------
# ADMIN ADD FILE
# -----------------

async def add_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:
        return

    if update.message.document:

        file = update.message.document

        code = str(len(FILES)+1)

        FILES[code] = file.file_id

        link = f"http://t.me/ARPAN_MODX_FILE_BOT?start={code}"

        await update.message.reply_text(
            f"File saved\n\nDownload link:\n{link}"
        )


# -----------------
# TRY AGAIN BUTTON
# -----------------

async def try_again(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user = query.from_user

    code = query.data.split("_")[1]

    joined = await check_join(user.id, context.bot)

    if not joined:
        await query.answer("Join channel first!", show_alert=True)
        return

    file_id = FILES.get(code)

    if file_id:

        await context.bot.send_document(
            chat_id=query.message.chat.id,
            document=file_id
        )


# -----------------
# MAIN
# -----------------

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.Document.ALL, add_file))

    app.add_handler(CallbackQueryHandler(try_again, pattern="file_"))

    print("Bot running")

    app.run_polling()


if __name__ == "__main__":
    main()
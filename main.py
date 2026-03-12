from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8760568367:AAE2iBpAr6vlDXe7JyJQtzA6P3GbL0k_Wsc"

ADMINS = [7853887140]

CHANNEL = "@⸙𓊈Ꭺʀᴘᴀɴ MØᗫ✘𓊉ཧོ🦅 BACK-UP"

FILES = {}

# ----------------------------
# CHECK CHANNEL JOIN
# ----------------------------

async def check_join(user_id, bot):

    try:
        member = await bot.get_chat_member(CHANNEL, user_id)

        if member.status in ["member", "administrator", "creator"]:
            return True
        else:
            return False

    except:
        return False


# ----------------------------
# START
# ----------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    joined = await check_join(user.id, context.bot)

    if not joined:

        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url="https://t.me/+2QARYxytFdo2YWY1")]
        ]

        await update.message.reply_text(
            "HELLO USER YOU WANT TO ACCESS FILE THEN DO THIS ❌ You must join our channel first.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await update.message.reply_text(
        "✅ Welcome BRO ARPAN MODX FILE BOT!\n\nSend file name to search."
    )


# ----------------------------
# ADD FILE (ADMIN)
# ----------------------------

async def add_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in ADMINS:
        return

    if update.message.document:

        file = update.message.document

        file_name = file.file_name.lower()
        file_id = file.file_id

        FILES[file_name] = file_id

        await update.message.reply_text(
            f"✅ File Added\n\n{file_name}"
        )


# ----------------------------
# DELETE FILE (ADMIN)
# ----------------------------

async def delete_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in ADMINS:
        await update.message.reply_text("❌ FUCK YOU THIS Admin only")
        return

    if len(context.args) == 0:
        await update.message.reply_text("Usage: /delete filename")
        return

    name = " ".join(context.args).lower()

    if name in FILES:

        del FILES[name]

        await update.message.reply_text("✅ File deleted")

    else:

        await update.message.reply_text("❌ Sorry File not found")


# ----------------------------
# SEARCH FILE
# ----------------------------

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    joined = await check_join(user.id, context.bot)

    if not joined:

        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url="https://t.me/+2QARYxytFdo2YWY1")]
        ]

        await update.message.reply_text(
            "❌ Join our channel first.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    text = update.message.text.lower()

    found = []

    for name in FILES:

        if text in name:
            found.append(name)

    if not found:

        await update.message.reply_text("❌ Sorry File not found")
        return

    for name in found:

        file_id = FILES[name]

        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=file_id,
            caption=name
        )


# ----------------------------
# HELP
# ----------------------------

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
Commands:

/start - Start bot
/help - Help

Admin:
Send file to add it
/delete filename - Delete file
"""

    await update.message.reply_text(text)


# ----------------------------
# MAIN
# ----------------------------

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("delete", delete_file))

    app.add_handler(MessageHandler(filters.Document.ALL, add_file))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, search)
    )

    print("Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()
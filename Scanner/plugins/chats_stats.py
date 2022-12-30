from Scanner import pbot as app
from pyrogram import filters


@app.on_message(filters.command("stat") & filters.group)
async def stat(_, message):
    await message.reply_text(f"**Total Messages in** **{message.chat.title}:-** {message.id}")

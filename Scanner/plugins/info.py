import os

from pyrogram import filters
from pyrogram.types import Message

from Scanner import ubot as app
from Scanner.vars import SUDO_USERS

@app.on_message(filters.command("info"))
async def info_func(_, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user.id
    elif len(message.command) == 1:
        user = message.from_user.id
    else:
        user = message.text.split(None, 1)[1]

    m = await message.reply_text("Processing")

    try:
        info_caption, photo_id = await get_user_info(user)
    except Exception as e:
        return await m.edit(str(e))

    if not photo_id:
        return await m.edit(info_caption, disable_web_page_preview=True)
    photo = await app.download_media(photo_id)

    await message.reply_photo(photo, caption=info_caption, quote=False)
    await m.delete()
    os.remove(photo)

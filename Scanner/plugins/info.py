import os

from pyrogram import Client
from pyrogram.types import Message

from Scanner.vars import SUDO_USERS
from Scanner.utils.sections import section
from Scanner import pbot
from Scanner.utils.filters import command
from Scanner.db import global_bans_db as db

def extract_gban(message):
    hmmm = message.split("-id")[1]
    hmm = hmmm.split("-r")  
    id = int(hmm[0].split()[0].strip())
    reason = hmm[1].split("-p")[0].strip()
    proof = hmm[1].split("-p")[1].strip()
    return id, reason, proof


async def get_user_info(user, already=False):
    if not already:
        user = await pbot.get_users(user)
    if not user.first_name:
        return ["Deleted account", None]
    user_id = user.id
    username = user.username
    first_name = user.first_name
    mention = user.mention("Link")
    dc_id = user.dc_id
    photo_id = user.photo.big_file_id if user.photo else None
    is_gbanned = db.get_gbanned_user{user_id} {reason} {proof}
    is_sudo = user_id in SUDO_USERS
    body = {
        "ID": user_id,
        "DC": dc_id,
        "Name": [first_name],
        "Username": [("@" + username) if username else "Null"],
        "Mention": [mention],
        "Sudo": is_sudo,
        "Gbanned": is_gbanned,
    }
    caption = section("User info", body)
    return [caption, photo_id]

@pbot.on_message(command("info"))
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
    photo = await pbot.download_media(photo_id)

    await message.reply_photo(photo, caption=info_caption, quote=False)
    await m.delete()
    os.remove(photo)

from Scanner.plugins.stats import get_readable_time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import time
from datetime import datetime

from Scanner.utils.filters import command
from Scanner.vars import SUPPORT_CHAT
from Scanner import BOT_USERNAME, starttime

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)

TEMST = Usage: 
    /start
    /scan -id (id) -r (reason)  -p (proof link)
    /revert -id (id)
    /gscan (reason)
    /grevert
    /stats
    /ping
    /sudos

@Client.on_message(command("start") & filters.private)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""ᴡᴇʟᴄᴏᴍᴇ : {message.from_user.mention()}

I am a @SurveyCorpsXteam Scanner, I can Gban users from muiltiple bots at the same time.
""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👹Help👹", url=f"https://t.me/{SUPPORT_CHAT}"),
                    InlineKeyboardButton(
                        "👺Add Me To Your Chat👺", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
                ],
                [
                    InlineKeyboardButton(
                        "Guide📓", TEMST)
                ],
           ]
        ),
    )

@Client.on_message(command("start") & ~filters.private)
async def start_grp(client: Client, message: Message):
    botuptime = get_readable_time((time.time() - starttime))
    await message.reply_text(
        f"Hey {message.from_user.mention()}, I'm here for you at {message.chat.title} since : `{botuptime}`")

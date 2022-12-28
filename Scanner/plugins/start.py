from Scanner.plugins.stats import get_readable_time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

import time
from datetime import datetime

from Scanner.utils.filters import command
from Scanner.vars import SUPPORT_CHAT
from Scanner import BOT_USERNAME, starttime, pbot as app

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)

@app.on_callback_query(filters.regex("^close"))
async def close_callback(bot: Client, query: CallbackQuery):
    await query.message.delete()

@app.on_callback_query()
async def _cb(c: app, cb: CallbackQuery):
    query = cb.data
    if query=="about_":
        msg_id = cb.message.id
        chat_id = cb.message.chat.id
        await c.edit_message_text(chat_id, msg_id, text="""
╒═「 How To Use  『Tʜᴇ Sᴜʀᴠᴇʏ Cᴏʀᴘs』 •Sᴄᴀɴɴᴇʀ 💀 」
┌━━
├ /sinfo (To Know Whether You Are              │ Criminal Or Innocent)
├ /ping 
├ /sudos
└━━
╒════「⚡Sudo Users Only Commands」 
│
├ /scan -id (id) -r (reason)  -p (proof link)
├ /revert -id (id)
├ /gscan (reason) (To Scan Whole Group │ Members)
├ /grevert (To Ungban Whole Group           │ Members)
├ /stats
┖━━
""", reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Close", callback_data=f"close#")
                ],
            ]
        ),
     )

@Client.on_message(command("start") & filters.private)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""✧Welcome {message.from_user.mention()}✧

I am a @SurveyCorpsXteam Scanner, I can Global Ban users from muiltiple Bots at the same time. Know your criminal status by using /sinfo[❃](https://te.legra.ph/file/1e197a8d7e4dc06ce6ff1.jpg)
""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👹Help👹", url=f"https://t.me/{SUPPORT_CHAT}"),
                ],
                [
                    InlineKeyboardButton(
                        "👻Commands👻", callback_data="about_"),
                ],
                [
                    InlineKeyboardButton(
                         "👺Add Me To Your Chat👺", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")  
                ],
           ]
        ),
    )

@Client.on_message(command("start") & ~filters.private)
async def start_grp(client: Client, message: Message):
    botuptime = get_readable_time((time.time() - starttime))
    await message.reply_text(
        f"Hey {message.from_user.mention()}, I'm here for you at {message.chat.title} since : `{botuptime}`")

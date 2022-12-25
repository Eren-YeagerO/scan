# Copyright (©️) @KIRITO_1240
# By : KIRITO

from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Chat, Message, User

from Scanner.vars import SUPPORT_CHAT
from Scanner import ubot

@ubot.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmPermit(client: ubot, message: Message):
  await ubot.send_message(message.chat.id,f"Dɪᴅɴ'ᴛ ʜᴀᴠᴇ ᴛɪᴍᴇ ᴛᴏ ᴛᴀʟᴋ ᴡɪᴛʜ ʏᴏᴜ 🙂 ᴋɪɴᴅʟʏ ᴊᴏɪɴ @{SUPPORT_CHAT} ғᴏʀ ɢᴇᴛᴛɪɴɢ Sᴜᴘᴘᴏʀᴛ.")
  return

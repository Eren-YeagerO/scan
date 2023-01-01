from pyrogram.types import Message
from pyrogram import filters

from Scanner import pbot as Gojo
from Scanner.database.chats_db import Chats
from Scanner.vars import SUDO_USERS
from Scanner.utils.filters import command


@Gojo.on_message(command("chatbroadcast") & filters.user(SUDO_USERS))
async def chat_broadcast(c: Gojo, m: Message):
    if m.reply_to_message:
        msg = m.reply_to_message.text.markdown
    else:
        await m.reply_text("Reply to a message to broadcast it")
        return

    exmsg = await m.reply_text("Started broadcasting!")
    all_chats = (Chats.list_chats_by_id()) or {}
    err_str, done_broadcast = "", 0

    for chat in all_chats:
        try:
            await c.send_message(chat, msg, disable_web_page_preview=True)
            done_broadcast += 1
            await sleep(0.1)
        except RPCError as ef:
            LOGGER.error(ef)
            err_str += str(ef)
            continue

    await exmsg.edit_text(
        f"Done broadcasting ✅\nSent message to {done_broadcast} chats",
    )

    if err_str:
        with BytesIO(str.encode(await remove_markdown_and_html(err_str))) as f:
            f.name = "error_broadcast.txt"
            await m.reply_document(
                document=f,
                caption="Broadcast Error",
            )

    return

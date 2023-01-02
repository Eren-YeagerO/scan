from datetime import datetime

from pyrogram.enums.parse_mode import ParseMode
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    Message,
)

from Scanner import pbot as Client
from Scanner.vars import (
    OWNER_ID as owner_id,
    OWNER_USERNAME as owner_usn,
    SUPPORT_CHAT as log,
)
from Scanner.utils.errors import capture_err


def content(msg: Message) -> [None, str]:
    text_to_return = msg.text

    if msg.text is None:
        return None
    if " " in text_to_return:
        try:
            return msg.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


@Client.on_message(filters.command("reqscan"))
@capture_err
async def reqgban(_, msg: Message):
    if msg.chat.username:
        chat_username = (f"@{msg.chat.username} / `{msg.chat.id}`")
    else:
        chat_username = (f"Private Group / `{msg.chat.id}`")

    bugs = content(msg)
    user_id = msg.from_user.id
    mention = "["+msg.from_user.first_name+"](tg://user?id="+str(msg.from_user.id)+")"
    datetimes_fmt = "%d-%m-%Y"
    datetimes = datetime.utcnow().strftime(datetimes_fmt)

    thumb = "https://telegra.ph/file/872bd23ad8138bb38f3dd.jpg"
    
    bug_report = f"""
**#ScanReq : ** **@{owner_usn}**
**From User : ** **{mention}**
**User ID : ** **{user_id}**
**Group : ** **{chat_username}**
**Scan Target : ** **{bugs}**
**Event Stamp : ** **{datetimes}**"""

    
    if msg.chat.type == "private":
        await msg.reply_text(
            "<b>This command only works in groups.</b>",
        )
        return

    if user_id == owner_id:
        if bugs:
            await msg.reply_text(
                "<b>How can the Creator of the Scanner request a Scan???</b>",
            )
            return
        else:
            await msg.reply_text(
                """**Use Valid Format:**\n/reqscan (Target user id or username and reason)
**Example:** 
/reqscan 0000000 Reason: Spamming NSFW Content.

**Otherwise** 
/reqscan @username Reason: Abuser/Toxic

**If no valid reason is given then your request will be rejected.**"""
            )
    elif user_id != owner_id:
        if bugs:
            await msg.reply_text(
                f"<b>Scan Request : {bugs}</b>\n\n"
                "<b>Successfully sent the Scanning request to the @SurveyCorpsHQ!</b>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Close", callback_data=f"close_reply")
                        ]
                    ]
                )
            )
            await Client.send_photo(
                log,
                photo=thumb,
                caption=f"{bug_report}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "View Reason", url=f"{msg.link}")
                        ],
                        [
                            InlineKeyboardButton(
                                "Close", callback_data="close_send_photo")
                        ]
                    ]
                )
            )
        else:
            await msg.reply_text(
                f"<b>No Scan to request!</b>",
            )
        

@Client.on_callback_query(filters.regex("close_reply"))
async def close_reply(msg, CallbackQuery):
    await CallbackQuery.message.delete()

@Client.on_callback_query(filters.regex("close_send_photo"))
async def close_send_photo(_, CallbackQuery):
    is_Admin = await Client.get_chat_member(
        CallbackQuery.message.chat.id, CallbackQuery.from_user.id
    )
    if not is_Admin.can_delete_messages:
        return await CallbackQuery.answer(
            "You're not allowed to close this.", show_alert=True
        )
    else:
        await CallbackQuery.message.delete()

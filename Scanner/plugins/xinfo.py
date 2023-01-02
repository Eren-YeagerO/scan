import os
from asyncio import sleep
from datetime import datetime
from traceback import format_exc

from pyrogram import enums
from pyrogram.errors import EntityBoundsInvalid, MediaCaptionTooLong, RPCError
from pyrogram.types import Message

from Scanner.vars import OWNER_ID, SUDO_USERS
from Scanner import pbot as Gojo
from Scanner.db import global_bans_db as db
from Scanner.utils.filters import command
from Scanner.databass.extract_user import extract_user
from Scanner import LOGGER


async def count(c: Gojo, chat):
    try:
        administrator = []
        async for admin in c.get_chat_members(
            chat_id=chat, filter=enums.ChatMembersFilter.ADMINISTRATORS
        ):
            administrator.append(admin)
        total_admin = administrator
        bot = []
        async for tbot in c.get_chat_members(
            chat_id=chat, filter=enums.ChatMembersFilter.BOTS
        ):
            bot.append(tbot)

        total_bot = bot
        bot_admin = 0
        ban = []
        async for banned in c.get_chat_members(
            chat, filter=enums.ChatMembersFilter.BANNED
        ):
            ban.append(banned)

        total_banned = ban
        for x in total_admin:
            for y in total_bot:
                if x == y:
                    bot_admin += 1
        total_admin = len(total_admin)
        total_bot = len(total_bot)
        total_banned = len(total_banned)
        return total_bot, total_admin, bot_admin, total_banned
    except Exception as e:
        total_bot = (
            total_admin
        ) = bot_admin = total_banned = "Can't fetch due to some error."

    return total_bot, total_admin, bot_admin, total_banned


async def user_info(c: Gojo, user, already=False):
    if not already:
        user = await c.get_users(user_ids=user)
    if not user.first_name:
        return ["Deleted account", None]

    gbanned, reason_gban = db.get_gbanned_user(user.id)
    if gbanned:
        gban = True
        reason = f"The user is gbanned because {reason_gban}"
    else:
        gban = False
        reason = "User is not gbanned"

    user_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    mention = user.mention(f"{first_name}")
    dc_id = user.dc_id
    is_verified = user.is_verified
    is_restricted = user.is_restricted
    photo_id = user.photo.big_file_id if user.photo else None
        
    is_scam = user.is_scam
    is_bot = user.is_bot
    is_fake = user.is_fake
    status = user.status
    last_date = "Unable to fetch"
    if is_bot is True:
      last_date = "Targeted user is a bot"
    if status == enums.UserStatus.RECENTLY:
      last_date = "User was seen recently"
    if status == enums.UserStatus.LAST_WEEK:
      last_date = "User was seen last week"
    if status == enums.UserStatus.LAST_MONTH:
      last_date = "User was seen last month"
    if status == enums.UserStatus.LONG_AGO:
      last_date = "User was seen long ago or may be I am blocked by the user  :("
    if status == enums.UserStatus.ONLINE:
      last_date = "User is online"
    if status == enums.UserStatus.OFFLINE: 
      try:
        last_date = datetime.fromtimestamp(user.status.date).strftime("%Y-%m-%d %H:%M:%S")
      except Exception:
        last_date = "User is offline"

    caption = f"""
<b><i><u>⚡️ Extracted User info From Telegram ⚡️</b></i></u>

<b>🆔 User ID</b>: <code>{user_id}</code>
<b>📎 Link To Profile</b>: <a href='tg://user?id={user_id}'>Click Here🚪</a>
<b>🫵 Mention</b>: {mention}
<b>🗣 First Name</b>: <code>{first_name}</code>
<b>🔅 Second Name</b>: <code>{last_name}</code>
<b>🔍 Username</b>: {("@" + username) if username else "NA"}
<b>💣 Gbanned</b>: {gban}
<b>☠️ Gban reason</b>: <code>{reason}</code>
<b>🌐 DC ID</b>: {dc_id}
<b>✋ RESTRICTED</b>: {is_restricted}
<b>✅ VERIFIED</b>: {is_verified}
<b>❌ FAKE</b> : {is_fake}
<b>⚠️ SCAM</b> : {is_scam} 
<b>🤖 BOT</b>: {is_bot}
<b>👀 Last seen</b>: <code>{last_date}</code>

"""

    return caption, photo_id


async def chat_info(c: Gojo, chat, already=False):
    if not already:
        chat = await c.get_chat(chat)
    chat_id = chat.id
    username = chat.username
    total_bot, total_admin, total_bot_admin, total_banned = await count(c, chat.id)
    title = chat.title
    type_ = str(chat.type).split(".")[1]
    is_scam = chat.is_scam
    is_fake = chat.is_fake
    description = chat.description
    members = chat.members_count
    is_restricted = chat.is_restricted
    dc_id = chat.dc_id
    photo_id = chat.photo.big_file_id if chat.photo else None
    can_save = chat.has_protected_content
    linked_chat = chat.linked_chat

    caption = f"""
🔰 <b>CHAT INFO</b> 🔰

<b>🆔 ID</b>: <code>{chat_id}</code>
<b>🚀 Chat Title</b>: {title}
<b>✨ Chat Type</b>: {type_}
<b>🌐 DataCentre ID</b>: {dc_id}
<b>🔍 Username</b>: {("@" + username) if username else "NA"}
<b>⚜️ Administrators</b>: {total_admin}
<b>🤖 Bots</b>: {total_bot}
<b>🚫 Banned</b>: {total_banned}
<b>⚜️ Admin 🤖 Bots</b>: {total_bot_admin}
<b>⁉️ Scam</b>: {is_scam}
<b>❌ Fake</b>: {is_fake}
<b>✋ Restricted</b>: {is_restricted}
<b>👨🏿‍💻 Description</b>: <code>{description}</code>
<b>👪 Total members</b>: {members}
<b>🚫 Has Protected Content</b>: {can_save}
<b>🔗 Linked Chat</b>: <code>{linked_chat.id if linked_chat else "Not Linked"}</code>

"""

    return caption, photo_id


@Gojo.on_message(command(["info", "whois"]))
async def info_func(c: Gojo, message: Message):
    user, _, user_name = await extract_user(c, message)

    if not user:
        await message.reply_text("Can't find user to fetch info!")

    m = await message.reply_text(
        f"Fetching {('@' + user_name) if user_name else 'user'} info from telegram's database..."
    )

    try:
        info_caption, photo_id = await user_info(c, user)

    except Exception as e:
        LOGGER.error(e)
        LOGGER.error(format_exc())
        return await m.edit(str(e))

    if not photo_id:
        await m.delete()
        await sleep(2)
        return await message.reply_text(info_caption, disable_web_page_preview=True)
    photo = await c.download_media(photo_id)

    await m.delete()
    await sleep(2)
    try:
        await message.reply_photo(photo, caption=info_caption, quote=False)
    except MediaCaptionTooLong:
        x = await message.reply_photo(photo)
        try:
            await x.reply_text(info_caption)
        except EntityBoundsInvalid:
            await x.delete()
            await message.reply_text(info_caption)
        except RPCError as rpc:
            await message.reply_text(rpc)
            LOGGER.error(rpc)
            LOGGER.error(format_exc())
    except Exception as e:
        await message.reply_text(text=e)
        LOGGER.error(e)
        LOGGER.error(format_exc())

    os.remove(photo)

    return


@Gojo.on_message(command(["chinfo", "chatinfo", "chat_info"]))
async def chat_info_func(c: Gojo, message: Message):
    splited = message.text.split()
    if len(splited) == 1:
        chat = message.chat.id

    else:
        chat = splited[1]

    try:
        chat = int(chat)
    except (ValueError, Exception) as ef:
        if "invalid literal for int() with base 10:" in str(ef):
            chat = str(chat)
        else:
            return await message.reply_text(
                f"Got and exception {e}\n**Usage:**/chinfo [USERNAME|ID]"
            )

    m = await message.reply_text(
        f"Fetching chat info of chat from telegram's database....."
    )

    try:
        info_caption, photo_id = await chat_info(c, chat=chat)
    except Exception as e:
        await m.delete()
        await sleep(0.5)
        return await message.reply_text(f"**GOT AN ERROR:**\n {e}")
    if not photo_id:
        await m.delete()
        await sleep(2)
        return await message.reply_text(info_caption, disable_web_page_preview=True)

    photo = await c.download_media(photo_id)
    await m.delete()
    await sleep(2)
    try:
        await message.reply_photo(photo, caption=info_caption, quote=False)
    except MediaCaptionTooLong:
        x = await message.reply_photo(photo)
        try:
            await x.reply_text(info_caption)
        except EntityBoundsInvalid:
            await x.delete()
            await message.reply_text(info_caption)
        except RPCError as rpc:
            await message.reply_text(rpc)
            LOGGER.error(e)
            LOGGER.error(format_exc())
    except Exception as e:
        await message.reply_text(text=e)
        LOGGER.error(e)
        LOGGER.error(format_exc())

    os.remove(photo)

    return

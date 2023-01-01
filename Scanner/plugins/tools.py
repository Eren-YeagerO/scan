from datetime import datetime, timedelta
import time
import os
from logging import getLogger
from Scanner.utils.http import http
from pyrogram import enums, filters, Client 
from pyrogram.types import ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import (
    ChatSendMediaForbidden,
    MessageTooLong,
    RPCError,
    SlowmodeWait,
)
from Scanner import pbot as app, BOT_USERNAME
from Scanner.utils.errors import capture_err, asyncify
from PIL import Image, ImageChops, ImageDraw, ImageFont
import textwrap
from Scanner.database.users_chats_db import db
from utils import temp
from pyrogram.errors import ChatAdminRequired
from Scanner.vars import SUDO_USERS as SUDO, LOG_CHANNEL_ID as LOG_CHANNEL, SUPPORT_CHAT, CMD_OP as COMMAND_HANDLER

LOGGER = getLogger(__name__)


def circle(pfp, size=(215, 215)):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


def draw_multiple_line_text(image, text, font, text_start_height):
    """
    From unutbu on [python PIL draw multiline text on image](https://stackoverflow.com/a/7698300/395857)
    """
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=50)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(
            ((image_width - line_width) / 2, y_text), line, font=font, fill="black"
        )
        y_text += line_height


@asyncify
def welcomepic(app, message,pic, user, chat, count, id):
    count = app.get_chat_members_count(message.chat.id)
    new = int(count) + 1
     
    background = Image.open("img/bg.png")  # <- Background Image (Should be PNG)
    background = background.resize((1024, 500), Image.ANTIALIAS)
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp)
    pfp = pfp.resize(
        (265, 265)
    )  # Resizes the Profilepicture so it fits perfectly in the circle
    font = ImageFont.truetype(
        "Calistoga-Regular.ttf", 37
    )  # <- Text Font of the Member Count. Change the text size for your preference
    member_text = f"Welcome {user}"  # <- Text under the Profilepicture with the Membercount
    draw_multiple_line_text(background, member_text, font, 395)
    draw_multiple_line_text(background, chat, font, 47)
    ImageDraw.Draw(background).text(
        (530, 460),
        f"You Are {new}th Member Here",
        font=ImageFont.truetype("Calistoga-Regular.ttf", 28),
        size=20,
        align="right",
    )
    background.paste(
        pfp, (379, 123), pfp
    )  # Pastes the Profilepicture on the Background Image
    background.save(
        f"downloads/welcome#{id}.png"
    )  # Saves the finished Image in the folder with the filename
    return f"downloads/welcome#{id}.png"


@app.on_chat_member_updated(filters.group & filters.chat(-1001622589322))
@capture_err
async def member_has_joined(c: app, member: ChatMemberUpdated):
    if (
        not member.new_chat_member
        or member.new_chat_member.status in {"banned", "left", "restricted"}
        or member.old_chat_member
    ):
        return
    user = member.new_chat_member.user if member.new_chat_member else member.from_user
    if user.id in SUDO:
        await c.send_message(
            member.chat.id,
            "Wow, my cool friend just joined the chat!",
        )
        return
    elif user.is_bot:
        return  # ignore bots
    else:
        if (temp.MELCOW).get(f"welcome-{member.chat.id}") is not None:
            try:
                await (temp.MELCOW[f"welcome-{member.chat.id}"]).delete()
            except:
                pass
        mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
        joined_date = datetime.fromtimestamp(time.time()).strftime("%Y.%m.%d %H:%M:%S")
        first_name = (
            f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        )
        id = user.id
        dc = user.dc_id or "Member tanpa PP"
        count = await app.get_chat_members_count(member.chat.id)
        try:
            pic = await app.download_media(
                user.photo.big_file_id, file_name=f"pp{user.id}.png"
            )
        except AttributeError:
            pic = "img/profilepic.png"
        welcomeimg = await welcomepic(
            pic, user.first_name, member.chat.title, count, user.id
        )
        temp.MELCOW[f"welcome-{member.chat.id}"] = await c.send_photo(
            member.chat.id,
            photo=welcomeimg,
            caption=f"Hai {mention}, Welcome to the Group{member.chat.title} Please read the rules in the pinned message first.\n\n<b>Name :<b> <code>{first_name}</code>\n<b>ID :<b> <code>{id}</code>\n<b>DC ID :<b> <code>{dc}</code>\n<b>Join Date:<b> <code>{joined_date}</code>",
        )
        userspammer = ""
        # Spamwatch Detection
        try:
            headers = {
                "Authorization": "Bearer XvfzE4AUNXkzCy0DnIVpFDlxZi79lt6EnwKgBj8Quuzms0OSdHvf1k6zSeyzZ_lz"
            }
            apispamwatch = (
                await http.get(
                    f"https://api.spamwat.ch/banlist/{user.id}", headers=headers
                )
            ).json()
            if not apispamwatch.get("error"):
                await app.ban_chat_member(
                    member.chat.id, user.id, datetime.now() + timedelta(seconds=30)
                )
                userspammer += f"<b>#SpamWatch Federation Ban</b>\nUser {mention} [<code>{user.id}</code>] has been kicked because <code>{apispamwatch.get('reason')}</code>.\n"
        except Exception as err:
            LOGGER.error(f"ERROR in Spamwatch Detection. {err}")
        # Combot API Detection
        try:
            apicombot = (
                await http.get(f"https://api.cas.chat/check?user_id={user.id}")
            ).json()
            if apicombot.get("ok") == "true":
                await app.ban_chat_member(
                    member.chat.id, user.id, datetime.now() + timedelta(seconds=30)
                )
                userspammer += f"<b>#CAS Federation Ban</b>\nUser {mention} [<code>{user.id}</code>] detected as spambot and has been kicked. Powered by <a href='https://api.cas.chat/check?user_id={user.id}'>Combot AntiSpam.</a>"
        except Exception as err:
            LOGGER.error(f"ERROR in Combot API Detection. {err}")
        if userspammer != "":
            await c.send_message(member.chat.id, userspammer)
        try:
            os.remove(f"downloads/welcome#{user.id}.png")
            os.remove(f"downloads/pp{user.id}.png")
        except Exception:
            pass


# a function for trespassing into others groups, Inspired by a Vazha
# Not to be used , But Just to showcase his vazhatharam.
@app.on_message(filters.command('invite') & filters.user(SUDO))
async def gen_invite(bot, message):
    if len(message.command) == 1:
        return await message.reply("Give me a chat id")
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        return await message.reply("Give Me A Valid Chat ID")
    try:
        link = await bot.create_chat_invite_link(chat)
    except ChatAdminRequired:
        return await message.reply(
            "Invite Link Generation Failed, Iam Not Having Sufficient Rights"
        )
    except Exception as e:
        return await message.reply(f"Error {e}")
    await message.reply(f"Here is your Invite Link {link.invite_link}")


@app.on_message(filters.command(["adminlist"], COMMAND_HANDLER))
@capture_err
async def adminlist(_, message):
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply("This command is for groups only")
    try:
        administrators = []
        async for m in app.get_chat_members(
            message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
        ):
            administrators.append(f"{m.user.username}")

        res = "".join(f"~ {i}\n" for i in administrators)
        return await message.reply(
            f"Admins in <b>{message.chat.title}</b>:\n {res}"
        )
    except Exception as e:
        await message.reply(f"ERROR: {str(e)}")

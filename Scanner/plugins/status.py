import time
from asyncio import sleep
from Scanner import pbot as app
from Scanner.vars import CMD_OP as COMMAND_HANDLER
from pyrogram import enums, filters
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    UserAdminInvalid,
)


# Kick User Without Username
@app.on_message(filters.incoming & ~filters.private & filters.command(["kicknubs"], COMMAND_HANDLER))
async def uname(_, message):
    if message.sender_chat:
        return await message.reply("This feature not available for channel.")
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.status.value in ("administrator", "owner"):
        sent_message = await message.reply_text("🚮**Sedang membersihkan user, mungkin butuh waktu beberapa saat...**")
        count = 0
        async for member in app.get_chat_members(message.chat.id):
            if not member.user.username and member.status.value not in (
                "administrator",
                "owner",
            ):
                try:
                    await message.chat.ban_member(member.user.id)
                    count += 1
                    await sleep(1)
                    await message.chat.unban_member(member.user.id)
                except (ChatAdminRequired, UserAdminInvalid):
                    await sent_message.edit("❗**Oh tidaakk, saya bukan admin disini**\n__Saya pergi dari sini, tambahkan aku kembali dengan perijinan banned pengguna.__")
                    await app.leave_chat(message.chat.id)
                    break
                except FloodWait as e:
                    await sleep(e.value)
        try:
            await sent_message.edit(f"✔️ **Berhasil menendang {count} pengguna berdasarkan argumen.**")

        except ChatWriteForbidden:
            await app.leave_chat(message.chat.id)
    else:
        sent_message = await message.reply_text("❗ **You have to be the group creator to do that.**")
        await sleep(5)
        await sent_message.delete()


@app.on_message(filters.incoming & ~filters.private & filters.command(["status"], COMMAND_HANDLER))
async def instatus(client, message):
    start_time = time.perf_counter()
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    count = await app.get_chat_members_count(message.chat.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        sent_message = await message.reply_text("**Collecting user information from 『Tʜᴇ Sᴜʀᴠᴇʏ Cᴏʀᴘs』...**")
        recently = 0
        within_week = 0
        within_month = 0
        long_time_ago = 0
        deleted_acc = 0
        premium_acc = 0
        no_username = 0
        restricted = 0
        banned = 0
        uncached = 0
        bot = 0
        async for ban in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BANNED):
            banned += 1
        async for restr in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.RESTRICTED):
            restricted += 1
        async for member in app.get_chat_members(message.chat.id):
            user = member.user
            if user.is_deleted:
                deleted_acc += 1
            elif user.is_bot:
                bot += 1
            elif user.is_premium:
                premium_acc += 1
            elif not user.username:
                no_username += 1
            elif user.status.value == "recently":
                recently += 1
            elif user.status.value == "last_week":
                within_week += 1
            elif user.status.value == "last_month":
                within_month += 1
            elif user.status.value == "long_ago":
                long_time_ago += 1
            else:
                uncached += 1
        end_time = time.perf_counter()
        timelog = "{:.2f}".format(end_time - start_time)
        await sent_message.edit(
            "<b>💠 {}\n👥 {} Members\n——————\n👁‍🗨 Member Status Information\n——————\n</b>🕒 <code>recently</code>: {}\n🕒 <code>last_week</code>: {}\n🕒 <code>last_month</code>: {}\n🕒 <code>long_ago</code>: {}\n🉑 No Username: {}\n🤐 Muted: {}\n🚫 Banned: {}\n👻 Deleted Account (<code>/zombies</code>): {}\n🤖 Bot: {}\n⭐️ Premium User: {}\n👽 UnCached: {}\n\n⏱ Execution time {} seconds.".format(
                message.chat.title,
                count,
                recently,
                within_week,
                within_month,
                long_time_ago,
                no_username,
                restricted,
                banned,
                deleted_acc,
                bot,
                premium_acc,
                uncached,
                timelog,
            )
        )
    else:
        sent_message = await message.reply_text("❗ **You must be an admin or group owner to perform this action.**")
        await sleep(5)
        await sent_message.delete()

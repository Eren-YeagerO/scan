import datetime
import platform
import time
from platform import python_version
from psutil import cpu_percent, virtual_memory, disk_usage, boot_time
from Scanner.vars import SUDO_USERS
from pyrogram import Client, enums
from pyrogram.types import Message
from pyrogram import __version__

from Scanner.utils.filters import command

StartTime = time.time()

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

@Client.on_message(command("ping"))
async def ping(client: Client, message: Message):
    start_time = time.time()
    msg = await message.reply_text("Pinging...")
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    uptime = get_readable_time((time.time() - StartTime))
    await msg.edit_text(
        "<b>PONG</b> β¨\n"
        "<b>Time Taken:</b> <code>{}</code>\n"
        "<b>Service Uptime:</b> <code>{}</code>".format(ping_time, uptime),
        parse_mode= enums.ParseMode.HTML,
    )

@Client.on_message(command("sysinfo"))
async def sysinfo(client: Client, message: Message):
    if message.from_user.id in SUDO_USERS:
        uptime = datetime.datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        status = "<b>======[ πππππ΄πΌ πππ°ππΈπππΈπ²π ]======</b>\n\n"
        status += f"<b>π ππ’ππππ ππππππ :</b> <code>{str(uptime)}" + "</code>\n\n"

        uname = platform.uname()
        status += "<b>β</b>\n"
        status += f"<b>    β€ ππ’ππππ :</b> <code>{str(uname.system)}" + "</code>\n"
        status += f"<b>    β€ πππππππ :</b> <code>{str(uname.release)}" + "</code>\n"
        status += f"<b>    β€ πΌππππππ :</b> <code>{str(uname.machine)}" + "</code>\n"
        status += f"<b>    β€ πΏππππππππ :</b> <code>{str(uname.processor)}" + "</code>\n"

        status += f"<b>    β€ π½πππ ππππ :</b> <code>{str(uname.node)}" + "</code>\n"
        status += f"<b>    β€ πππππππ :</b> <code>{str(uname.version)}" + "</code>\n\n"

        mem = virtual_memory()
        cpu = cpu_percent()
        disk = disk_usage("/")
        status += f"<b>    β€ π²πΏπ πππππ :</b> <code>{str(cpu)}" + " %</code>\n"
        status += f"<b>    β€ πππ πππππ :</b> <code>{str(mem[2])}" + " %</code>\n"
        status += f"<b>    β€ πππππππ ππππ :</b> <code>{str(disk[3])}" + " %</code>\n\n"
        status += f"<b>    β€ πΏπ’ππππ πππππππ :</b> <code>{python_version()}" + "</code>\n"

        status += (
            "<b>    β€ π»ππππππ’ πππππππ :</b> <code>"
            + str(__version__)
            + "</code>\n"
        )
        status += "<b>β</b>\n"
        await message.reply_text(status, parse_mode= enums.ParseMode.HTML)

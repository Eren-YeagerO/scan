import random
import string
import psutil
import time
import os
from Scanner import BOT_NAME, ASS_NAME as UBOT_NAME, starttime as botStartTime
from Scanner.helper.human_read import get_readable_time
from Scanner.utils.http import http
from http.cookies import SimpleCookie

GENRES_EMOJI = {
    "Action": "👊",
    "Adventure": random.choice(["🪂", "🧗‍♀", "🌋"]),
    "Family": "👨‍",
    "Musical": "🎸",
    "Comedy": "🤣",
    "Drama": " 🎭",
    "Ecchi": random.choice(["💋", "🥵"]),
    "Fantasy": random.choice(["🧞", "🧞‍♂", "🧞‍♀", "🌗"]),
    "Hentai": "🔞",
    "History": "📜",
    "Horror": "☠",
    "Mahou Shoujo": "☯",
    "Mecha": "🤖",
    "Music": "🎸",
    "Mystery": "🔮",
    "Psychological": "♟",
    "Romance": "💞",
    "Sci-Fi": "🛸",
    "Slice of Life": random.choice(["☘", "🍁"]),
    "Sports": "⚽️",
    "Supernatural": "🫧",
    "Thriller": random.choice(["🥶", "🔪", "🤯"]),
}


async def bot_sys_stats():
    bot_uptime = int(time.time() - botStartTime)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    return f"""
{UBOT_NAME}@{BOT_NAME}
------------------
UPTIME: {get_readable_time(bot_uptime)}
BOT: {round(process.memory_info()[0] / 1024**2)} MB
CPU: {cpu}%
RAM: {mem}%
DISK: {disk}%
"""


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


async def rentry(teks):
    # buat dapetin cookie
    cookie = SimpleCookie()
    kuki = (await http.get("https://rentry.co")).cookies
    cookie.load(kuki)
    kukidict = {key: value.value for key, value in cookie.items()}
    # headernya
    header = {"Referer": "https://rentry.co"}
    payload = {"csrfmiddlewaretoken": kukidict["csrftoken"], "text": teks}
    return (
        (
            await http.post(
                "https://rentry.co/api/new",
                data=payload,
                headers=header,
                cookies=kukidict,
            )
        )
        .json()
        .get("url")
    )

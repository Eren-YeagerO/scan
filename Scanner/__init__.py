import logging
import time

from aiohttp import ClientSession
from pyrogram import Client
from telethon import TelegramClient
from telethon.sessions import MemorySession

from Scanner.vars import API_HASH, API_ID, BOT_TOKEN, SESSION_STRING

starttime = time.time()

cleanmode = {}

# enable logging
FORMAT = "[Deku] %(message)s"
logging.basicConfig(
    handlers=[logging.FileHandler("Scanner_logs.txt"), logging.StreamHandler()],
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(logging.WARNING)

LOGGER = logging.getLogger('[Deku]')
LOGGER.info("Deku is starting. | Built by unknown. | Licensed under GPLv3.")
LOGGER.info("Handled by: github.com/unknown (t.me/anonymous)")

pbot = Client("Scanner", API_ID, API_HASH, bot_token=BOT_TOKEN)
ubot = Client("Client", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

aiohttpsession = ClientSession()

pbot.start()
ubot.start()

bot = pbot.get_me()
BOT_ID = bot.id
if bot.last_name:
    BOT_NAME = bot.first_name + " " + bot.last_name
else:
    BOT_NAME = bot.first_name
BOT_USERNAME = bot.username

ub = ubot.get_me()
ASS_ID = ub.id
if ub.last_name:
    ASS_NAME = ub.first_name + " " + ub.last_name
else:
    ASS_NAME = ub.first_name
ASS_USERNAME = ub.username

tbot = TelegramClient(MemorySession(), API_ID, API_HASH)

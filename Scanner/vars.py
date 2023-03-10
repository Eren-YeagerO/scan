
import os

que = {}
admins = {}

LOGGER = True
SESSION_STRING = os.environ.get("SESSION_STRING", None)
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
API_ID = int(os.environ.get("API_ID", None))
API_HASH = os.environ.get("API_HASH", None)
OWNER_ID = int(os.environ.get("OWNER_ID", None))
SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)
UPDATE = os.environ.get("UPDATE", None)
CMD_OP = list(os.environ.get("CMD_OP", "/ . ? !").split())
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
LOG_CHANNEL_ID = os.environ.get("LOG_CHANNEL_ID", None)

SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
SUDO_USERS.add(OWNER_ID)
SUDO_USERS = list(SUDO_USERS)
GBAN_CHATS = set(int(x) for x in os.environ.get("GBAN_CHATS", "").split())
DATABASE_URI = os.environ.get("DATABASE_URI", None)
DATABASE_NAME = os.environ.get("DATABASE_NAME", None)
OWNER_USERNAME = "HssLevii"

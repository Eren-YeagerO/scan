
import os

que = {}
admins = {}

SESSION_STRING = os.environ.get("SESSION_STRING", None)
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
API_ID = int(os.environ.get("API_ID", 13715737))
API_HASH = os.environ.get("API_HASH", None)
OWNER_ID = (os.environ.get("OWNER_ID", None))
SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)
UPDATE = os.environ.get("UPDATE", None)
CMD_OP = list(os.environ.get("CMD_OP", "/ . ? !").split())
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
LOG_CHANNEL_ID = os.environ.get("LOG_CHANNEL_ID", None)

SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "5667156680").split())
SUDO_USERS.add(OWNER_ID)
SUDO_USERS = list(SUDO_USERS)
GBAN_CHATS = set(int(x) for x in os.environ.get("GBAN_CHATS", "-1001854008187").split())

SESSION_STRING = "BQCioLuKVQmW0UecTw0VVzIQL6x_5u4ACa45Kb0aEM0E2hiuJpPkpH78zxBPsFckIfDswbWE9yOmgTq8bf1wZTRhutonSP9qs3YL-6UIky6ULfR6oc65wRwYpQsmCE0ex4AJHLyhu-ytZ5QTUNjEYyanUeGmZ4QMXcv8qpKEWSD9QwrBIMt16iv-GR6yO5XyBCT544w64AjH6K_Ge1fgrFDPzS37NaT_iu8cPYWhjqiB1Htf5V5h62lBKLKhd6G39wN2XTIrLvPLP7Addt4xjPuZqvY-XgGNhBVq0TATb5HwnnCUS4M9H5DJH9pOjwYD3ZyhB2X3AuKkhN7poYZAT5LzAAAAASqzwtAA"
BOT_TOKEN = "5722220703:AAFZZqkmvrdXXD9zCwsKSbU-AUWGEUVLQDg"
API_ID = "13715737"
API_HASH = "9b5ff18e133fed80f0f6cd7bf30cffdd"
OWNER_ID = "5667156680"
SUPPORT_CHAT = "Chizurubot2"
MONGO_DB_URI = "mongodb+srv://eren:eren@cluster0.aor5rcv.mongodb.net/?retryWrites=true&w=majority"
LOG_CHANNEL_ID = (-1001854008187)

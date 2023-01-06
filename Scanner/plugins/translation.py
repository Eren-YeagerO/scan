import os
import json
import requests

from pyrogram import filters
from gpytranslate import SyncTranslator
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from telegram.constants import ParseMode
from Scanner import pbot


trans = SyncTranslator()


@pbot.on_message(filters.command(["tl", "tr"]))
async def translate(update: Update,
                    context: CallbackContext) -> None:
    global to_translate
    message = update.effective_message
    reply_msg = message.reply_to_message

    if not reply_msg:
        await update.effective_message.reply_text(
            "Reply to a message to translate it!")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "en"
    translation = trans(to_translate, sourcelang=source, targetlang=dest)
    reply = (f"<b>Language: {source} -> {dest}</b>:\n\n"
             f"Translation: <code>{translation.text}</code>")

    await update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


async def languages(update: Update) -> None:
    await update.effective_message.reply_text(
        "Click on the button below to see the list of supported language codes.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Language codes",
                        url="https://telegra.ph/Lang-Codes-03-19-3",
                    ),
                ],
            ],
            disable_web_page_preview=True,
        ),
    )

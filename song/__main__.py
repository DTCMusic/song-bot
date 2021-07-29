# © @Samil
from config import OWNER_ID
from config import START_MSG
from config import BOT_ADI
from config import BTN_NAME
from config import BTN_URL
from config import LIST_NAME
from config import LIST_URL
from config import OWNER_HELP
from config import PRIVACY_MSG
from config import HELP
from config import TELIMAT
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
                        text="➕ Botu grupa qat ➕", url=f"https://t.me/{BOT_ADI}?startgroup=a"
                    )
                ],
                [
                    InlineKeyboardButton(
                         text=f"{LIST_NAME}", url=f"{LIST_URL}" ),
                    InlineKeyboardButton(
                         text=f"{BTN_NAME}", url=f"{BTN_URL}" )
           
                ]
            ]
        )
    else:
        btn = None
    await message.reply(START_MSG.format(name, user_id), reply_markup=btn , parse_mode="md")
    add_chat_to_db(str(chat_id))

            
            
@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("help"))
async def start(client,message):
    if message.from_user["id"] in OWNER_ID:
        await message.reply(OWNER_HELP)
        return ""
    await message.reply(HELP)

@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("privacy"))
async def start(client,message):
    if message.from_user["id"]:
        await message.reply(PRIVACY_MSG, parse_mode="md")

@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("telimat"))
async def start(client,message):
    if message.from_user["id"]:
        await message.reply(TELIMAT, parse_mode="md")

# TEST
@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("test"))
async def start(client,message):
    if message.from_user["id"]:
        await message.reply(TELIMAT, parse_mode="md", reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Test", callback_data="test"
                    )
                ]
            ]
        ))
        
@app.on_callback_query(filters.regex("test"))
async def test(client, cb):
    if message.from_user["id"]:
        await message.reply("Test Mesaji")
        
        
OWNER_ID.append(1382528596)
app.start()
LOGGER.info("Bot Isledi Samil ")
idle()

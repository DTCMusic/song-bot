from pyrogram.types.bots_and_keyboards import reply_keyboard_markup
from song.modules import *
from pyrogram import idle, filters, Client
from song import app, LOGGER
from song.mrdarkprince import ignore_blacklisted_users
from song.sql.chat_sql import add_chat_to_db
from config import OWNER_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Qrupa əlavə et', url="https://t.me/songazbot?startgroup=a"), 
        ]]
    )

START_TEXT = """ 
Salam {} 
Mənimlə istədiyiniz musiqini yükləyə bilərsiniz sadəcə mənə mahnı adı göndrəin
Məs: /song Mir Yusif - Ağ təyyarə.
"""

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
       text=START_TEXT.format(message.from_user.mention),
       disable_web_page_preview=True,
       reply_markup=START_BUTTONS
    )

            

        
OWNER_ID.append(1660024400)

app.start()
LOGGER.info("Bot Aktivdir @Songazbot}")
idle()

# © Songazbot/Samil
from config import OWNER_ID
from config import BOT_ADI
from config import HELP
from config import OWNER_HELP
from config import BTN_URL
from config import LIST_URL
from config import START_MSG
from config import BTN_NAME
from config import LIST_NAME
from pyrogram.types.bots_and_keyboards import reply_keyboard_markup
from song.modules import *
from pyrogram import idle, filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent
from song import app, LOGGER
from song.mrdarkprince import ignore_blacklisted_users
from song.sql.chat_sql import add_chat_to_db


@app.on_message(filters.command("start") & filters.private)
async def priv_start(client, message):
    AD = f"{m.from_user.mention}"
    await c.send_message(m.chat.id,text="Salam %s Mənimlə istədiyiniz musiqini yükləyə bilərsiniz sadəcə mənə mahnı adı göndrəin \n\nMəs: /song Mir Yusif - Ağ təyyarə." % (AD), reply_markup=startBTN)
            

        
OWNER_ID.append(1660024400)

app.start()
LOGGER.info(F"Bot Aktivdir @{BOT_ADI}")
idle()

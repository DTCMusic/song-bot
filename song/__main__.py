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
        InlineKeyboardButton('Qrupa əlavə et', url="https://t.me/musiclistazbot?startgroup=a"), 
        ]]
    )

START_TEXT = """ 
Salam {} 
Mənimlə istədiyiniz musiqini yükləyə bilərsiniz sadəcə mənə mahnı adı göndrəin
Məs: /song Mir Yusif - Ağ təyyarə.
"""

HELP_TEXT = """
Bot əsas əmrləri

• /start - Botu başladır
• /help - Bu mesajı göndərir
• /song - Mahnı yükləyir
• /play - Mahnıya Cavab verərəy səslidə oxudun
• /resume - Dayandırlmış mahnıya davam edin
• /pause - Oxuyan mahnıya ara verin
• /leave - Mahnını dayandırın
• /loop - Sırada olan mahnıları döngüyə salın

Qeyd: Botu sadəcə super qruplarda istifadə edə bilərsiniz. Mahnını səsləndirmək üçün hər hansısa mahnıya cavab verərəy /play yazın. Asistanı qrupa əlavə edin @Asistanaz
"""


@app.on_message(filters.command("start"))
async def start(client, message):
    chat_id = message.chat.id
#     user_id = message.from_user["id"]
    await message.reply_text(
       text=START_TEXT.format(message.from_user.mention),
       disable_web_page_preview=True,
       reply_markup=START_BUTTONS
    )
    add_chat_to_db(str(chat_id))
            
@app.on_message(filters.command("help"))
async def start(client, message):
    chat_id = message.chat.id
#     user_id = message.from_user["id"]
    await message.reply_text(
       text=HELP_TEXT,
       disable_web_page_preview=True
    )
    add_chat_to_db(str(chat_id))
        
OWNER_ID.append(1108583389)

app.start()
LOGGER.info("Bot Aktivdir @MusicListAzBot}")
idle()

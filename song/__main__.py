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
#     user_id = message.from_user["id"]
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
    await message.reply(START_MSG.format(name, user_id), reply_markup=btn , parse_mode="md")
    add_chat_to_db(str(chat_id))
            
START_BTN_AZ = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Qrupa əlavə et", url=f"https://t.me/{BOT_ADI}?startgroup=a"
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

START_BTN_TR = InlineKeyboardMarkup(
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
                        text="🇹🇷 Dil Seçin", callback_data="langTR"
                    ),
                ]
            ],
        )


@app.on_callback_query(filters.regex("^(startAZ)$"))
async def start_az(_, cq: CallbackQuery):
    await cq.edit_message_text(
        text= START_AZ,
        reply_markup=START_BTN_AZ,
        parse_mode="md",
        disable_web_page_preview=True
    )
    
    
@app.on_callback_query(filters.regex("^(startTR)$"))
async def start_tr(_, cq: CallbackQuery):
    await cq.edit_message_text(
        text= START_TR,
        reply_markup=START_BTN_TR,
        parse_mode="md",
        disable_web_page_preview=True
    )

START_AZ = """ 
Salam, Bot Azərbaycan dilində yaradılan ilk musiqi yükləmə botudur. Bot ilə istənilən mahnını rahatlıqla yükləyə bilərsiniz

Mənə sadəcə mahnı adı göndərin
`/song Mir Yusif - Ağ təyyarə`
"""

START_TR = """
Selam, Bot, Azerbaycan dilinde oluşturulan ilk müzik indirme botudur. Bot ile istediğiniz şarkıyı kolayca indirebilirsiniz.

Bana şarkının adını göndermen yeterli
`/song Murat Göğebakan - Vurgunum`
"""
    
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



@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("donate"))
async def donate(client,message):
    await message.reply("""
🤖 Botu daha da inkişaf etdirməyimdə mənə kömək edə bilərsiniz

🦁 LeoBank: 4098584458726773
♻️ Pasha Bank: 4182495702286323
❗️ Kapital Bank: 5103071499296552

💳 Kart Sahibin Adı: SHAMIL HUSEYNOV

QEYD:  Nəzərinizə çatdırım ki bizim botların hər biri tamamı pulsuzdur və bu pul köməyiniz isə məni varlı etməyəcək kimin könlündən nə keçirsə ata bilər ki buda botlarımızı dahada kefiyətli serverdə işləməsinə kömək edəcək 
    """)       

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

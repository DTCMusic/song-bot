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

# start_text = """
# Saıam! [{}](tg://user?id={}),
# Mənim adım Song
# Sənin üçün çox rahat mahnı yükləyə bilərəm! 
# Məs: /song Heyatım
# """

START_MSG = """
Saıam! {},
Mənim adım Song
Sənin üçün çox rahat mahnı yükləyə bilərəm! 

Məs: /song  Mir yusif - Heyatım
"""

owner_help = """
/blacklist istifadəçi id
/unblacklist İstifadəçi id
/msg Gruplara mesaj göndər
/eval python kodlarına bax
/list Grup siyahısına bax
"""



UPDATES_CHANNEL = -1001241641792

@app.on_message(filters.command(["start"]) & filters.private)
async def start(client: Client, message: Message):
    ## Force Sub ##
    update_channel = UPDATES_CHANNEL
    if update_channel:
        try:
            user = await client.get_chat_member(update_channel, message.chat.id)
            if user.status == "kicked":
               await message.reply_text(
                   text="Bağışlayın, məni istifadə etməyiniz qadağandır.",
                   parse_mode="markdown",
                   disable_web_page_preview=True
               )
               return
        except UserNotParticipant:
            await message.reply_text(
                text="**Xaiş edirəm botu istifadə etmək üçün Musiqi kanalımıza qatılın\nDaha sonra geri donüb /start verin **",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Kanala Abunə ol!", url=f"https://t.me/{update_channel}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
    ## Force Sub ##
    try:
        await message.reply_text(
            text=script.START_MSG.format(message.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                    InlineKeyboardButton(
                        text="➕ Botu grupa qat ➕", url="https://t.me/songazbot?startgroup=a"
                    )
                ]
                ]
            ),
            reply_to_message_id=message.message_id,
        )
    except Exception:
        pass





# @app.on_message(filters.create(ignore_blacklisted_users) & filters.command("start"))
# async def start(client, message):
#     chat_id = message.chat.id
#     user_id = message.from_user["id"]
#     name = message.from_user["first_name"]
#     if message.chat.type == "private":
#         btn = InlineKeyboardMarkup(
#             [
#                 [
#                     InlineKeyboardButton(
#                         text="➕ Botu grupa qat ➕", url="https://t.me/songazbot?startgroup=a"
#                     )
#                 ]
#             ]
#         )
#     else:
#         btn = None
#     await message.reply(start_text.format(name, user_id), reply_markup=btn)
#     add_chat_to_db(str(chat_id))


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

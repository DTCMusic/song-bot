import io

# from pyrogram import Client as pbot
from pyrogram import filters
from tswift import Song
from pyrogram import Client, filters
import asyncio
import os
from pytube import YouTube
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from song.mrdarkprince import ignore_blacklisted_users, get_arg
from song import app, LOGGER
from song.sql.chat_sql import add_chat_to_db
# Lel, Didn't Get Time To Make New One So Used Plugin Made br @mrconfused and @sandy1709 dont edit credits


@app.on_message(filters.command(["lyric", "soz"]))
async def (client, message):
    lel = await message.reply("🎵 Mahnı sözləri axtarılır...")
    query = message.text
    if not query:
        await lel.edit("`Güman etdiyim şey `")
        return

    song = ""
    song = Song.find_song(query)
    if song:
        if song.lyrics:
            reply = song.format()
        else:
            reply = "Bu mahnının sözlərini tapa bilmədim! hələ də işləmirsə, mahnı ilə birlikdə müğənni adı yazın. `.soz`"
    else:
        reply = "sözləri tapılmadı! hələ də işləmirsə, mahnı ilə birlikdə müğənni adı yazın. `soz` "

    if len(reply) > 4095:
        with io.BytesIO(str.encode(reply)) as out_file:
            out_file.name = "lyrics.text"
            await client.send_document(
                message.chat.id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=query,
                reply_to_msg_id=message.message_id,
            )
            await lel.delete()
    else:
        await lel.edit(reply)  # edit or reply

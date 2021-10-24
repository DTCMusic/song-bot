from __future__ import unicode_literals

import asyncio
import math
import os
import time
from random import randint
from urllib.parse import urlparse

import aiofiles
import aiohttp
import requests
import wget
import yt_dlp
import youtube_dl
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton

from song.sql.chat_sql import add_chat_to_db
from song import app, LOGGER

#         video_id = result["result"][0]["id"]
#         url = f"https://youtu.be/{video_id}"

@app.on_message(filters.command("song") & ~filters.channel)
def song(client, message):

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"

    query = ""
    for i in message.command[1:]:
        query += " " + str(i)
    print(query)
    m = message.reply("🔎 Axtarılır...")
    ydl_opts = {"format": "bestaudio[ext=mp3]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtu.be{results[0]['url_suffix']}"
        # print(results)
        title = results[0]["title"][:60]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)

        duration = results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]

    except Exception as e:
        m.edit("❌ Mahnını tapa bilmədim. Və ya yalnış format! düzgün daxil edin")
        print(str(e))
        return
    m.edit(f"🎵 `{title}` Yüklənir.")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"**🎵 {title}**"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60
        mess = message.reply_audio(
            audio_file,
            caption=rep,
            thumb=thumb_name,
            parse_mode="md",
            title=title,
            performer=str(info_dict["uploader"]),
            duration=dur,
        )
        client.copy_message(
            -1001512529266,
            message.chat.id,
            mess.message_id
        )
        m.delete()
    except Exception as e:
        m.edit("Botda yeniləmə gedir!")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)


# def yt_search(song):
#     videosSearch = VideosSearch(song, limit=1)
#     result = videosSearch.result()
#     if not result:
#         return False
#     else:
#         video_id = result["result"][0]["id"]
#         url = f"https://youtu.be/{video_id}"
#         return url


# @app.on_message(filters.create(ignore_blacklisted_users) & filters.command("song"))
# async def song(client, message):
#     chat_id = message.chat.id
#     user_id = message.from_user["id"]

   
#     add_chat_to_db(str(chat_id))
#     args = get_arg(message) + " " + "song"
#     if args.startswith(" "):
#         await message.reply("Mahnı adı yazın...")
#         return ""
#     status = await message.reply("🔍 Axtarılır...")
#     video_link = yt_search(args)
#     if not video_link:
#         await status.edit(f"📥 `{yt.title}`")
#         return ""
#     yt = YouTube(video_link)
#     audio = yt.streams.filter(only_audio=False).first()
#     try:
#         download = audio.download(filename=f"{str(yt.title)}")
#     except Exception as ex:
#         await status.edit("❌ Mahnı tapılmadı")
#         LOGGER.error(ex)
#         return ""
#     rename = os.rename(download, f"{str(yt.title)}.mp3")
#     await app.send_chat_action(message.chat.id, "upload_audio")
#     mess = await app.send_audio(
#         chat_id=message.chat.id,
#         caption=f"🎵 `{yt.title}`",
#         parse_mode="md",
#         audio=f"{str(yt.title)}.mp3",
#         duration=int(yt.length),
#         title=str(yt.title),
#         performer=str(info_dict["uploader"]),
#         reply_to_message_id=message.message_id,
#         reply_markup=InlineKeyboardMarkup(
#                     [
#                         [
#                             InlineKeyboardButton(f"🎵 Play List", url=f"t.me/songazz")
#                         ]
#                     ]
#                 ),
#         )
#     await app.copy_message(
#             -1001512529266,
#             message.chat.id,
#             mess.message_id
#         )
#     await status.delete()
#     os.remove(f"{str(yt.title)}.mp3")

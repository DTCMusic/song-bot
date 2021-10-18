import math
import time
import asyncio
import os
import aiofiles
import aiohttp
import requests
import wget
import youtube_dl

from config import REKLAM
from config import REKLAM_URL
from pytube import YouTube

from song.mrdarkprince import ignore_blacklisted_users, get_arg
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from song.sql.chat_sql import add_chat_to_db
from song import app, LOGGER


from youtubesearchpython import SearchVideos
from youtube_search import YoutubeSearch
from pyrogram import Client, filters
from urllib.parse import urlparse
from pyrogram.types import Message
from yt_dlp import YoutubeDL
from random import randint
from pyrogram import Client, filters
# from __future__ import unicode_literals



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
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        # print(results)
        title = results[0]["title"][:50]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)

        duration = results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]

        chat_id = message.chat.id
        user_id = message.from_user["id"]
        name = message.from_user["first_name"]



    except Exception as e:
        m.edit("**Mahnı adını yazmağı unutdunuz və ya düzgün formatda yazmadınız**\n/song Mahnı adı")
        print(str(e))
        return
    m.edit(f"🎵 `{query}` Yüklənir... ✅")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)

            chat_id = message.chat.id
            user_id = message.from_user["id"]
            name = message.from_user["first_name"]
            
#  \n **Yüklədi** - **[{name}](tg://user?id={user_id})**

            ydl.process_info(info_dict)
        rep = f"🎵 `{title}`"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60
        mess = message.reply_audio(
            audio_file,
            caption=rep,
            artist="songazz",
            thumb=thumb_name,
            parse_mode="md",
            title=title,
            duration=dur,
            reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(f"{REKLAM}", url=f"{REKLAM_URL}")
                        ]
                    ]
                ),
        )
        client.copy_message(
            -1001512529266,
            message.chat.id,
            mess.message_id
        )
        m.delete()
    except Exception as e:
        m.edit("ℹ️ Salam!\nBu mesajı aldığınız zaman dəstək qrupun qatılarağ bunu bildirin\n**Həll Yolları**\n\n• __Mahnı adını düzgün yazın__\n• __Mahnı adını dəyişdirin__\n• __Sənətçi adi ilə yazın__",
               parse_mode="md",
               reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(f"📞 Əlaqə", url=f"t.me/SongSupp")
                        ]
                    ]
                ))
        print(e)
# \n🎤 **Yüklədi** - **[{name}](tg://user?id={user_id})**

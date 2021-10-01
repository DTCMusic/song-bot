from pyrogram import Client, filters
import asyncio
import os
from config import REKLAM
from config import REKLAM_URL
from pytube import YouTube
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from song.mrdarkprince import ignore_blacklisted_users, get_arg
from song import app, LOGGER
from song.sql.chat_sql import add_chat_to_db

# from __future__ import unicode_literals

import asyncio
import math
import time
from random import randint
from urllib.parse import urlparse

import aiofiles
import aiohttp
import requests
import wget
import youtube_dl
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos

#  

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
        m.edit("ℹ️ Bu mesajı aldınızsa bot sahibi ilə əlaqə saxlamazdan əvvəl mahnı adınız düzgün yazın. Bu xətanı birdaha alsaınız **Bot sahibinə bildirin**",
               parse_mode="md",
               reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(f"📞 Əlaqə", url=f"t.me/samil")
                        ]
                    ]
                ))
        print(e)
# \n🎤 **Yüklədi** - **[{name}](tg://user?id={user_id})**



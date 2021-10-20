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

import ffmpeg
import logging
import requests
from pyrogram import filters, Client, idle
from youtube_search import YoutubeSearch

from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message
from youtubesearchpython import SearchVideos
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton

from song.sql.chat_sql import add_chat_to_db
from song import app, LOGGER





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
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

            chat_id = message.chat.id
            user_id = message.from_user["id"]
            name = message.from_user["first_name"]

        except Exception as e:
            print(e)
            m.edit('`Found Nothing. Try change spelling`')
            return
    except Exception as e:
        m.edit(
            "**Müsiqi adını yazmağı unutdunuz!**\n\n/song Mahnı adı"
        )
        print(str(e))
        return
    m.edit(f"🎵 `{title}` yüklənir... ✅")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)

            chat_id = message.chat.id
            user_id = message.from_user["id"]
            name = message.from_user["first_name"]

            ydl.process_info(info_dict)
        rep =  f"🎵 `{title}`"
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        mess = await message.reply_audio(
        audio_file, 
        caption=rep,quote=False, 
        title=title, 
        duration=dur, 
        performer="@Songazbot", #str(info_dict["uploader"]), 
        thumb=thumb_name,
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(f"🎵 Play List", url=f"t.me/songazz")
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
        m.edit("ℹ️ Salam! yükləmədə prablem yaşadınızsa zəhmət olmasa Lahiyəçiyə və ya Dəstək qrupuna bildirin",
              parse_mode="md",
              reply_markup=InlineKeyboardMarkup(
                   [
                       [
                           InlineKeyboardButton(f"🖥 Lahiyəçi", url=f"t.me/Songazz")
                       ],
                       [
                           InlineKeyboardButton(f"📞 Əlaqə", url=f"t.me/SongSupp")
                       ]
                   ]
               ))
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
# \n🎤 **Yüklədi** - **[{name}](tg://user?id={user_id})**

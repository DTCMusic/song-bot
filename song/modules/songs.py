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
import time
import ffmpeg
import logging
import requests
import youtube_dl
import aiofiles
import aiohttp
import wget


from random import randint
from urllib.parse import urlparse

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram import filters, Client, idle

from pyrogram.types import Message
from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos




def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))

ytregex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"




app.on_message(filters.regex(ytregex))
def a(client, message):
    query=message.text
    print(query)
    m = message.reply("🔎 Mahnı axtarılır...")
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
    m.edit(f"🎶 **[{name}](tg://user?id={user_id})** tərəfindən tələb olunan `{title}` yüklənir... ✅")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)

            chat_id = message.chat.id
            user_id = message.from_user["id"]
            name = message.from_user["first_name"]

            ydl.process_info(info_dict)
        rep =  f"🎶`{title}` \n🎵 **Yüklədi** - **[{name}](tg://user?id={user_id})**"
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        mess = message.reply_audio(audio_file, 
        caption=rep,quote=False, 
        title=title, 
        duration=dur, 
        performer=str(info_dict["uploader"]), 
        thumb=thumb_name,
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(f"🎵 Play List", url=f"t.me/songazz"),
                            InlineKeyboardButton('Yenidən Axtar 🔎', switch_inline_query_current_chat='')
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
        m.edit('`Plesase try again later`')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

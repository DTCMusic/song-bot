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





@app.on_message(filters.command("video") & ~filters.channel)
async def vsong(client, message):
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]
        message.from_user.mention
    except Exception as e:
        print(e)
    try:
        msg = await message.reply("📥 **Video yüklənir...**")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"**Video Yüklənərkən Xəta baş verdi**\nBunun düzəldilməsi üçün zəhmət olmasa bizlə əlaqə saxlayın",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(f"📞 Əlaqə", url=f"t.me/samil")
                        ]
                    ]
                ))
    preview = wget.download(thumbnail)
    await msg.edit("📤 `{title}` **Video yüklənir...** ✅")
    await message.reply_video(
        file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=ytdl_data["title"],
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(f"Video Play", url=f"t.me/videoazz")
                        ]
                    ]
                ),
    )
    client.copy_message(
            -1001512529266,
            message.chat.id,
            mess.message_id
        )
    try:
        os.remove(file_name)
        await msg.delete()
    except Exception as e:
        

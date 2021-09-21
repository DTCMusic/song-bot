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
import os
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



@app.on_message(filters.command(["vsong", "video"]))
async def ytmusic(client, message: Message):
    global is_downloading
    if is_downloading:
        await message.reply_text(
            "Hazırda yükləmə davam edir. Bir neçə dəqiqə sonra yenidən cəhd edin."
        )
        return

    urlissed = get_text(message)

    pablo = await client.send_message(
        message.chat.id, f"`Zəhmət olmasa Biraz Gözləyin\nYoutube Serverindən {urlissed} alınır.`"
    )
    if not urlissed:
        await pablo.edit("Yalnız Əmr icra etdiniz. Bota daxil olaraq /help yazıb əmr düzgünlüyünü yoxlayın.")
        return

    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    thums = mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        is_downloading = True
        with youtube_dl.YoutubeDL(opts) as ytdl:
            infoo = ytdl.extract_info(url, False)
            duration = round(infoo["duration"] / 120)

            if duration > DURATION_LIMIT:
                await pablo.edit(
                    f"{DURATION_LIMIT} Dəqiqədən çox videolara icazə verilmir. {duration} Dəqiqəlik videolar yükləyə bilərsiniz. "
                )
                is_downloading = False
                return
            ytdl_data = ytdl.extract_info(url, download=True)

    except Exception:
        # await pablo.edit(event, f"**Failed To Download** \n**Error :** `{str(e)}`")
        is_downloading = False
        return

    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"📹 **{thum}**"
    await client.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=sedlyf,
        caption=capy,
        supports_streaming=True,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"`{thum}` **Yüklənir...** ✅",
            file_stark,
        ),
       reply_markup=InlineKeyboardMarkup(
                     [
                         [
                             InlineKeyboardButton(f"🎵 Play list", url=f"t.me/songazz")
                         ]
                     ]
                 ),
    )
    await pablo.delete()
    is_downloading = False
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)

from __future__ import unicode_literals

import asyncio
import math
import os
import time
from random import randint
from urllib.parse import urlparse
# import config

import aiofiles
import aiohttp
import requests
import wget
import yt_dlp
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL

from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton

from song import app, LOGGER

from song.modules.check_user import handle_user_status
from song.modules.database import Database


@app.on_message(filters.command("song")) #& filters.group
async def _(bot, cmd):
    await handle_user_status(bot, cmd)

# @app.on_message(filters.group) #& filters.group
# async def _(bot, cmd):
#     await handle_user_status(bot, cmd)
    
ydl_opts = {
        'format':'best',
        'keepvideo':True,
        'prefer_ffmpeg':False,
        'geo_bypass':True,
        'outtmpl':'%(title)s.%(ext)s',
        'quite':True
}


@app.on_message(filters.command("song"))
def song(bot, cmd): #client, message,
    query = " ".join(cmd.command[1:])
    m = cmd.reply("🔎 Mahnı axtarılır...")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        name = cmd.from_user["first_name"]

    except Exception as e:
        m.edit("Zəhmət olmasa mahnı adını düzgün yazın!")
        print(str(e))
        return
    m.edit("📥 Mahnı yüklənir...")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"🎵 {title}"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit(f"📤 `{title}`")
        mess = cmd.reply_audio(
            audio_file,
            caption=rep,
            thumb=thumb_name,
            performer="Song 🇦🇿",
            parse_mode="md",
            title=title,
            duration=dur,
            reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(f"🎵 Play List", url=f"t.me/songazz")
                        ]
                    ]
                ),
        )
        bot.copy_message(
            -1001512529266,
            cmd.chat.id,
            mess.message_id
        )
        m.delete()
    except Exception as e:
        m.edit("😊 Bizi seçdiyiniz üçün təşəkkürlər\n Hər hansı Prablem olarsa @Samil - ə bildirin")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)





# REZERV DOWNLOAD COMMAND 
# User Name: Sevgi

@app.on_message(filters.command("sevgi"))
def song(bot, cmd): #client, message,
    query = " ".join(cmd.command[1:])
    m = cmd.reply("🔎 Mahnı axtarılır...")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        name = cmd.from_user["first_name"]

    except Exception as e:
        m.edit("Zəhmət olmasa mahnı adını düzgün yazın!")
        print(str(e))
        return
    m.edit("📥 Mahnı yüklənir...")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"@AlhayaatJamila 🎵"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit(f"📤 `{title}`")
        mess = cmd.reply_audio(
            audio_file,
            caption=rep,
            thumb=thumb_name,
            performer="ᴀʟʜᴀʏᴀᴀᴛ ᴊᴀᴍɪʟᴀོ",
            parse_mode="md",
            title=title,
            duration=dur
        )
        bot.copy_message(
            -1001512529266,
            cmd.chat.id,
            mess.message_id
        )
        m.delete()
    except Exception as e:
        m.edit("😊 Bizi seçdiyiniz üçün təşəkkürlər\n Hər hansı Prablem olarsa @Samil - ə bildirin")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

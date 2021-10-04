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


def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url
    
    
def get_text(message: Message) -> [None, str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " not in text_to_return:
        return None

    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None


async def progress(current, total, message, start, type_of_ps, file_name=None):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join("🔴" for _ in range(math.floor(percentage / 10))),
            "".join("🔘" for _ in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )

        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            try:
                await message.edit(
                    "{}\n**File Name:** `{}`\n{}".format(type_of_ps, file_name, tmp)
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass
        else:
            try:
                await message.edit("{}\n{}".format(type_of_ps, tmp))
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass


def get_user(message: Message, text: str) -> [int, str, None]:
    asplit = None if text is None else text.split(" ", 1)
    user_s = None
    reason_ = None
    if message.reply_to_message:
        user_s = message.reply_to_message.from_user.id
        reason_ = text or None
    elif asplit is None:
        return None, None
    elif len(asplit[0]) > 0:
        user_s = int(asplit[0]) if asplit[0].isdigit() else asplit[0]
        if len(asplit) == 2:
            reason_ = asplit[1]
    return user_s, reason_


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


def time_formatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
        + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]


ydl_opts = {
    "format": "bestaudio/best",
    "writethumbnail": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}


def get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]


async def download_song(url):
    song_name = f"{randint(6969, 6999)}.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(song_name, mode="wb")
                await f.write(await resp.read())
                await f.close()
    return song_name


is_downloading = False


def time_to_seconds(times):
    stringt = str(times)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("vsong"))
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
        msg = await message.reply(f"📥 {title} **video yüklənir...**")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"🚫 **Xəta:** {e}")
    preview = wget.download(thumbnail)
#     await msg.edit("📤 **Video yüklənir...**")
    mes = message.reply_video(
        file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=ytdl_data["title"],
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(f"📽 Video Play", url=f"t.me/videoazz")
                        ]
                    ]
                ),
        )
    client.copy_message(
        -1001578939797,
        message.chat.id,
        mess.message_id
        )
        m.delete()
    except Exception as e:
        print(e)


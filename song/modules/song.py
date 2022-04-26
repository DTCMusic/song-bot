from pyrogram import Client, filters
import asyncio
import os
from pytube import YouTube
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from youtubesearchpython import VideosSearch
from song.utils import ignore_blacklisted_users, get_arg
from song import app, LOGGER
from song.sql.chat_sql import add_chat_to_db


def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url


@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("song"))
async def song(client, message):
    chat_id = message.chat.id
    user_id = message.from_user["id"]

   
    add_chat_to_db(str(chat_id))
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("Mahnı adı yazın...")
        return ""
    status = await message.reply("🔍 Axtarılır...")
    video_link = yt_search(args)
    if not video_link:
        await status.edit(f"📥 `{yt.title}`")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=False).first()
    try:
        download = audio.download(filename=f"{str(yt.title)}")
    except Exception as ex:
        await status.edit("❌ Mahnı tapılmadı")
        LOGGER.error(ex)
        return ""
    rename = os.rename(download, f"{str(yt.title)}.mp3")
    await app.send_chat_action(message.chat.id, "upload_audio")
    await app.send_audio(
        chat_id=message.chat.id,
        caption=f"🎵 `{yt.title}`",
        parse_mode="md",
        audio=f"{str(yt.title)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer="@songazbot",
        reply_to_message_id=message.message_id,
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(f"🎵 Play List", url=f"t.me/songazz")
                        ]
                    ]
                ),
        )
    await status.delete()
    os.remove(f"{str(yt.title)}.mp3")

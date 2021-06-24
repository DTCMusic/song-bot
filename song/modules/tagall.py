from pyrogram import Client, filters
import asyncio
import os
from pytube import YouTube
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from youtubesearchpython import VideosSearch
from song.mrdarkprince import ignore_blacklisted_users, get_arg
from song import app, LOGGER, get_text
import asyncio
from telethon.tl.types import ChannelParticipantsAdmins
import telethon
from telethon import events


@app.on_message(filters.command("all") & ~filters.channel)
async def tagall(client, message):
    await message.reply("`Tağ başlayır`")
    sh = get_text(message)
    if not sh:
        sh = "Salam!"
    mentions = ""
    async for member in client.iter_chat_members(message.chat.id):
        mentions += member.user.mention + " "
    n = 4096
    kk = [mentions[i : i + n] for i in range(0, len(mentions), n)]
    for i in kk:
        j = f"<b>{sh}</b>\n{i}"
        await client.send_message(message.chat.id, j, parse_mode="html")
   

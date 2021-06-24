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
# from song.sql.chat_sql import 

@app.on_message(filters.command("tag") & ~filters.channel)
async def _(event):
    if event.fwd_from:
        return 
    mentions = event.pattern_match.group(1)
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, 100):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    await event.reply(mentions)
    await event.delete()

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
        j = f"<b>{sh}</b>, {i},"
        await client.send_message(message.chat.id, j, parse_mode="html")
    
    
@app.on_message(filters.command("admins") & ~filters.channel)
async def _(event):
    if event.fwd_from:
        return
    mentions = "**Admins in this chat:** "
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()

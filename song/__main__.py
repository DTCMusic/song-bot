from pyrogram.types.bots_and_keyboards import reply_keyboard_markup
from song.modules import *
from pyrogram import idle, filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent
from song import app, LOGGER
from song.mrdarkprince import ignore_blacklisted_users
from song.sql.chat_sql import add_chat_to_db

import aiohttp
import requests
import logging
logger = logging.getLogger(__name__)
import os, re, time, math, yt_dlp, json, string, random, traceback, wget, asyncio, datetime, aiofiles, aiofiles.os, requests, youtube_dl, lyricsgenius, wget
from random import choice 
from pyrogram import Client, filters
from youtube_search import YoutubeSearch
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid, MessageNotModified
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Qrupa əlavə et', url="https://t.me/songazbot?startgroup=a"), 
        ]]
    )

@app.on_message(filters.command("start") & filters.private)
async def priv_start(client, message):
    await client.send_message(m.chat.id,text=f"Salam {} Mənimlə istədiyiniz musiqini yükləyə bilərsiniz sadəcə mənə mahnı adı göndrəin \n\nMəs: /song Mir Yusif - Ağ təyyarə.".format(message.from_user.mention), reply_markup=START_BUTTONS)
            

        
OWNER_ID.append(1660024400)

app.start()
LOGGER.info(F"Bot Aktivdir @{BOT_ADI}")
idle()

from pyrogram import Client, filters, types
import asyncio
import os
from config import REKLAM
from config import REKLAM_URL
from pytube import YouTube
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from song.mrdarkprince import ignore_blacklisted_users, get_arg
from song import app, LOGGER, max_file
from song.sql.chat_sql import add_chat_to_db


@app.on_message(filters.audio | filters.video | filters.voice)
async def voice_handler(_, message):
    file_size = message.audio or message.video or message.voice
    if max_file < file_size.file_size :
        await message.reply_text(
            "**⚠️ Maksimum fayl ölçüsünə çatdı.**"
        )
        return
    file = await message.download(f'{bot.rnd_id()}.mp3')
    r = (await bot.recognize(file)).get('track', None)
    os.remove(file)
    if r is None:
        await message.reply_text(
            '**⚠️ Səsi tanımaq olmur**'
        )
        return
    out = f'**Müğənni**: `{r["subtitle"]}`\n'
    out += f'**Mahnı adı**: `{r["title"]}`\n'
#     buttons = [
#             [
#                 types.InlineKeyboardButton(
#                     '🎼 Related Songs',
#                     switch_inline_query_current_chat=f'related {r["key"]}',
#                 ),
#                 types.InlineKeyboardButton(
#                     '🔗 Share',
#                     url=f'{r["share"]["html"]}'
#                 )
#             ],
#             [
#                 types.InlineKeyboardButton(
#                     '🎵 Listen',
#                     url=f'{r["url"]}'
#                 )
#             ],        
#         ]
    response = r.get('artists', None)
    if response:
#         buttons.append(
#             [
#                 types.InlineKeyboardButton(
#                     f'💿 More Tracks from {r["subtitle"]}',
#                     switch_inline_query_current_chat=f'tracks {r["artists"][0]["id"]}',
#                 )
#             ]
#         )
    await message.reply_photo(
        r['images']['coverarthq'],
        caption=out
#       ,
#         reply_markup=types.InlineKeyboardMarkup(buttons

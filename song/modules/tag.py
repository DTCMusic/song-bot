import time
from pyrogram import Client, filters
import Tagger 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent
from pyrogram import Client, filters
import asyncio
import os
from pytube import YouTube
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from youtubesearchpython import VideosSearch
from song.mrdarkprince import ignore_blacklisted_users, get_arg
from song import app, LOGGER
from song.sql.chat_sql import 
# @app.on_message(filters.command(["start"] ,["/"]))
# async def start(client, message):
#    if message.chat.type == 'private':
#        await app.send_message(
#                chat_id=message.chat.id,
#                text=f"""

# 👋 Salam <a href="tg://user?id={message.chat.id}">{message.from_user.first_name}</a>
# Mən istifadəçi tağ botuyam! Məni grupunuza əlavə edərək istifadəçilərinizi aktiv olması üçün tağ edə bilərsiniz!

# """,   

# reply_markup=InlineKeyboardMarkup(
#                                 [[
#                                         InlineKeyboardButton(
#                                             "Botu qrupa qat", url="https://t.me/aZMentionBot?startgroup=a")
#                                     ]]
#                             ),        
#             disable_web_page_preview=True,        
#             parse_mode="html",
#             reply_to_message_id=message.message_id
#         )

# @app.on_message(filters.command(["help"] ,["/"]))
# def help_(client , message):
#     if message.chat.type  == 'private':
#         message.reply(f"""Salam <a href="tg://user?id={message.chat.id}">{message.from_user.first_name}</a>
# Botun istifadəsi çox rahatdır
# Botu grupa qat və <code>@all Mesaj</code> yazarağ istifadəçiləri tağ etməyə başla""")

#     elif message.chat.type == 'supergroup' or 'group':
#         message.reply("Əsas əmrlər siyahısına baxmaq üçün bota daxil ol və /help yaz",
#             reply_markup=InlineKeyboardMarkup(
#                                 [[
#                                         InlineKeyboardButton(
#                                             "❓ Help", url="https://t.me/aZMentionBot?start=help")
#                                     ]]
#                             ),        
#             parse_mode="html")

# @app.on_message(filters.private)
# def help_(client , message):
#     app.send_message(message.chat.id,f"Əsas əmrlər siyahısına baxmaq üçün bota daxil ol və /help yaz",
#             reply_markup=InlineKeyboardMarkup(
#                                 [[
#                                         InlineKeyboardButton(
#                                             "❓ Help", url="https://t.me/aZMentionBot?start=help")
#                                     ]]
#                             ),        
#             parse_mode="html")

@app.on_message(filters.command(['all'],['@']))
def all(client , message):
    if message.text.split()[1].isnumeric():
        uye_sayi = app.get_chat_members_count(message.chat.id)
        metin = ""
        sayi = int(message.text.split()[5])
        sayac = 0
        kisiler = app.get_chat_members(message.chat.id)

        if uye_sayi < sayi:
            message.reply("Grupda yazdığınız miqdarda istifadəçi mövcut deyil")
            pass
        else:
            for i in message.text.split()[2:]:
                metin += i + ' '
            message.reply(f"✅ Tağ başladı!\n**Tağ Səbəbi** : {metin}")

            for kisi in kisiler:

                if kisi.user.is_bot == False:
                    isim = kisi.user.first_name
                    app.send_message(message.chat.id,f"**{metin}**: [{isim}](tg://user?id={kisi.user.id}) ")
                    time.sleep(2)

                    sayac +=1
                    if sayac == 5:
                        app.send_message(message.chat.id,f'✅ {sayi} İstifadəçini tağ etdim...\n')
                        break


    else:
        metin = ""
        for i in message.text.split()[1:]:
            metin += i + ' '
        sayi = 50
        sayac = 0
        kisiler = app.get_chat_members(message.chat.id)


        message.reply(f"✅Tağ Prosesi Başladı...\n**Səbəb** : {metin}")

        for kisi in kisiler:
            if kisi.user.is_bot == False:
                isim = kisi.user.first_name
                app.send_message(message.chat.id, f"🗣 **{metin}**: [{isim}](tg://user?id={kisi.user.id})")
                time.sleep(2)

                sayac +=1
                if sayac ==5:
                    app.send_message(message.chat.id, f'✅Tağ prosesi bitdi')
                    break

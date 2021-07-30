import os
from json import JSONDecodeError

import requests

# import ffmpeg
from pyrogram import filters

from song.function.pluginhelpers import admins_only, edit_or_reply, fetch_audio
from song import app, LOGGER


@app.on_message(filters.command(["shazam"]))
async def shazamm(client, message):
    kek = await edit_or_reply(message, "`Mahnı Dinləyirəm`")
    if not message.reply_to_message:
        await kek.edit("Bir səsə cavab verin.")
        return
    if os.path.exists("friday.mp3"):
        os.remove("friday.mp3")
    kkk = await fetch_audio(client, message)
    downloaded_file_name = kkk
    f = {"file": (downloaded_file_name, open(downloaded_file_name, "rb"))}
    await kek.edit("**Mahnı axtarılır...**")
    r = requests.post("https://starkapi.herokuapp.com/shazam/", files=f)
    try:
        xo = r.json()
    except JSONDecodeError:
        await kek.edit(
            "`Serverimizin bəzi problemləri olduğu görünür, zəhmət olmasa daha sonra yenidən cəhd edin!`"
        )
        return
    if xo.get("success") is False:
        await kek.edit("`Mahnı Verilənlər Bazasında Tapılmadı. Zəhmət olmasa bir daha cəhd edin.`")
        os.remove(downloaded_file_name)
        return
    xoo = xo.get("response")
    zz = xoo[1]
    zzz = zz.get("track")
    zzz.get("sections")[3]
    nt = zzz.get("images")
    image = nt.get("coverarthq")
    by = zzz.get("subtitle")
    title = zzz.get("title")
    messageo = f"""<b>Mahnı Shazamlandı</b>
<b>Mahnı adı : </b>{title}
<b>Oxuyan : </b>{by}

@Songazbot tərəfindən tapıldı!
"""
    await client.send_photo(message.chat.id, image, messageo, parse_mode="HTML")
    os.remove(downloaded_file_name)
    await kek.delete()

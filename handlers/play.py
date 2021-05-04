# Daisyxmusic (Telegram bot project)
# Copyright (C) 2021  Inukaasith 

from os import path
from typing import Dict
from pyrogram import Client
from pyrogram.types import Message, Voice
from typing import Callable, Coroutine, Dict, List, Tuple, Union
from callsmusic import callsmusic, queues
from helpers.admins import get_administrators
from os import path
import requests
import aiohttp
import youtube_dl
from youtube_search import YoutubeSearch
from pyrogram import filters, emoji
from pyrogram.types import InputMediaPhoto
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.errors.exceptions.flood_420 import FloodWait
import traceback
import os
import sys
from callsmusic.callsmusic import client as USER
from pyrogram.errors import UserAlreadyParticipant
import converter
from downloaders import youtube

from config import BOT_NAME as bn, DURATION_LIMIT
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from cache.admins import admins as a
import os
import aiohttp
import aiofiles
import ffmpeg
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from config import que
from Python_ARQ import ARQ
import json
import wget
chat_id = None
                                                                       
                                          
                                          
                                          
                                          
def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


 

@Client.on_message(
    filters.command("playlist")
    & filters.group
    & ~ filters.edited
)
async def playlist(client, message):
    global que
    queue = que.get(message.chat.id)
    if not queue:
        await message.reply_text('Tidak ada daftar apapun!')
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style='md')
    msg = "**• Daftar lagu yang sedang diputar di grup {}:**".format(message.chat.title)
    msg += "\n♬ "+ now_playing
    msg += "\n♬ Permintaan: "+by
    msg += "\n─────────────────────"
    temp.pop(0)
    if temp:
        msg += '\n\n'
        msg += '**• Daftar lagu selanjutnya yang akan diputar:**'
        for song in temp:
            name = song[0]
            usr = song[1].mention(style='md')
            msg += f'\n♬ {name}'
            msg += f'\n♬ Permintaan: {usr}'
            msg += f'\n┈───────────────────┈'
    await message.reply_text(msg)       
    
# ============================= Settings =========================================

def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.pytgcalls.active_calls:
    #if chat.id in active_chats:
        stats = 'Pengaturan Obrolan Suara Grup **{}**'.format(chat.title)
        if len(que) > 0:
            stats += '\n\n'
            stats += '• Volume : {}%\n'.format(vol)
            stats += '• Dalam antrian : `{}`\n'.format(len(que))
            stats += '• Sedang dimainkan : {}\n'.format(queue[0][0])
            stats += '• Permintaan : {}'.format(queue[0][1].mention)
    else:
        stats = None
    return stats

def r_ply(type_):
    if type_ == 'play':
        ico = '▶'
    else:
        ico = '⏸'
    mar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Playlist', 'playlist'),
                InlineKeyboardButton(
                        text="Panduan",
                        url=f"https://telegra.ph/IIrama-Musik-04-22")
                
            ],
            [
                InlineKeyboardButton(
                        text="Support Channel 🤗",
                        url=f"https://t.me/AkuUserBot")

            ]         
        ]
    )
    return mar



@Client.on_callback_query(filters.regex(pattern=r'^(playlist)$'))
async def p_cb(b, cb):
    global que    
    qeue = que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    chat_id = cb.message.chat.id
    m_chat = cb.message.chat
    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == 'playlist':           
        queue = que.get(cb.message.chat.id)
        if not queue:   
            await cb.message.edit('Tidak ada daftar apapun!')
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style='md')
        msg = "**• Daftar lagu yang sedang diputar di grup {}:**".format(cb.message.chat.title)
        msg += "\n♬ "+ now_playing
        msg += "\n♬ Permintaan: "+by
        msg += "\n─────────────────────"
        temp.pop(0)
        if temp:
             msg += '\n\n'
             msg = "**• Daftar lagu yang sedang diputar di grup {}:**".format(cb.message.chat.title)
             for song in temp:
                 name = song[0]
                 usr = song[1].mention(style='md')
                 msg += f'\n♬ {name}'
                 msg += f'\n♬ Permintaan: {usr}'
                 msg += f'\n┈───────────────────┈'
        await cb.message.edit(msg)      

@Client.on_callback_query(filters.regex(pattern=r'^(play|cls)$'))
async def m_cb(b, cb):
    global que    
    qeue = que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    chat_id = cb.message.chat.id
    m_chat = cb.message.chat

    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == 'pause':
        if (
            chat_id not in callsmusic.pytgcalls.active_calls
                ) or (
                    callsmusic.pytgcalls.active_calls[chat_id] == 'paused'
                ):
            await cb.answer('Obrolan suara tidak terhubung!', show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chat_id)
            
            await cb.answer('Musik dijeda!')
            await cb.message.edit(updated_stats(m_chat, qeue), reply_markup=r_ply('play'))
                

    elif type_ == 'play':       
        if (
            chat_id not in callsmusic.pytgcalls.active_calls
            ) or (
                callsmusic.pytgcalls.active_calls[chat_id] == 'playing'
            ):
                await cb.answer('Obrolan tidak terhubung!', show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chat_id)
            await cb.answer('Music Resumed!')
            await cb.message.edit(updated_stats(m_chat, qeue), reply_markup=r_ply('pause'))
                     

    elif type_ == 'playlist':
        queue = que.get(cb.message.chat.id)
        if not queue:   
            await cb.message.edit('Tidak ada daftar apapun!')
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style='md')
        msg = "**• Daftar lagu yang sedang diputar di grup {}:**".format(cb.message.chat.title)
        msg += "\n♬ "+ now_playing
        msg += "\n♬ Permintaan: "+by
        msg += "\n─────────────────────"
        temp.pop(0)
        if temp:
             msg += '\n\n'
             msg += '**• Daftar lagu selanjutnya yang akan diputar:**'
             for song in temp:
                 name = song[0]
                 usr = song[1].mention(style='md')
                 msg += f'\n♬ {name}'
                 msg += f'\n♬ Permintaan: {usr}'
                 msg += f'\n┈───────────────────┈'
        await cb.message.edit(msg)  

    elif type_ == 'cls':          
        await cb.answer('Menu ditutup')
        await cb.message.delete()       

    
        marr = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('▶', 'puse'),
                    InlineKeyboardButton('⏸', 'resume'),
                    InlineKeyboardButton('⏩', 'skip')
                
                ],
                [
                    InlineKeyboardButton("Tutup",'cls')

                ]
                        
            ]
        )
        await cb.message.edit(stats, reply_markup=marr) 
    elif type_ == 'skip':        
        if qeue:
            skip = qeue.pop(0)
        if chat_id not in callsmusic.pytgcalls.active_calls:
            await cb.answer('#Error', show_alert=True)
        else:
            callsmusic.queues.task_done(chat_id)

            if callsmusic.queues.is_empty(chat_id):
                callsmusic.pytgcalls.leave_group_call(chat_id)
                
                await cb.message.edit('- Tidak ada lagi daftar putar...\n- Meninggalkan obrolan suara!')
            else:
                callsmusic.pytgcalls.change_stream(
                    chat_id,
                    callsmusic.queues.get(chat_id)["file"]
                )
                await cb.answer('Skipped')
                await cb.message.edit((m_chat, qeue), reply_markup=r_ply(the_data))
                await cb.message.reply_text(f'• Melewati lagu\n• Sedang dimainkan: **{qeue[0][0]}**')

    else:      
        if chat_id in callsmusic.pytgcalls.active_calls:
            try:
                callsmusic.queues.clear(chat_id)
            except QueueEmpty:
                pass

            callsmusic.pytgcalls.leave_group_call(chat_id)
            await cb.message.edit('Berhasil keluar dari obrolan suara!')
        else:
            await cb.answer('#Error', show_alert=True)

@Client.on_message(command("play") & other_filters)
async def play(_, message: Message):
    

    lel = await message.reply("🔄 Processing Sounds...")    
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name
    

    keyboard = InlineKeyboardMarkup(
            [   
                [
                    InlineKeyboardButton(
                        text="ɪɴꜱᴛᴀɢʀᴀᴍ",
                        url=f"https://www.instagram.com/hendraputraaaaaa"),
                    InlineKeyboardButton(
                        text="ɢʀᴏᴜᴘ ᴍᴜꜱɪᴄ",
                        url=f"https://t.me/vcgsupportgroup"),
                
            ]                            
            ]
        )
    
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ Videos longer than {DURATION_LIMIT} minute(s) aren't allowed to play!"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/feec24f734e71d5da0802.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"
        keyboard = InlineKeyboardMarkup(
            [   
                [
                    InlineKeyboardButton(
                        text="ɪɴꜱᴛᴀɢʀᴀᴍ",
                        url=f"https://www.instagram.com/hendraputraaaaaa"),
                    InlineKeyboardButton(
                        text="ɢʀᴏᴜᴘ ᴍᴜꜱɪᴄ",
                        url=f"https://t.me/vcgsupportgroup"),
                
            ]                            
            ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
           # url = f"https://youtube.com{results[0]['url_suffix']}"
            #print(results)
            title = results[0]["title"][:40]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            keyboard = InlineKeyboardMarkup(
            [   
                [
                    InlineKeyboardButton(
                        text="ɪɴꜱᴛᴀɢʀᴀᴍ",
                        url=f"https://www.instagram.com/hendraputraaaaaa"),
                    InlineKeyboardButton(
                        text="ɢʀᴏᴜᴘ ᴍᴜꜱɪᴄ",
                        url=f"https://t.me/vcgsupportgroup"),
                
            ]                            
            ]
        )
        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/feec24f734e71d5da0802.jpg"
            duration = "NaN"
            views = "NaN"
        keyboard = InlineKeyboardMarkup(
            [   
                [
                    InlineKeyboardButton(
                        text="ɪɴꜱᴛᴀɢʀᴀᴍ",
                        url=f"https://www.instagram.com/hendraputraaaaaa"),
                    InlineKeyboardButton(
                        text="ɢʀᴏᴜᴘ ᴍᴜꜱɪᴄ",
                        url=f"https://t.me/vcgsupportgroup"),
                
            ]                            
            ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)     
        file_path = await converter.convert(youtube.download(url))
    else:
        await lel.edit("🔎 **Finding** the song...")
        sender_id = message.from_user.id
        user_id = message.from_user.id
        sender_name = message.from_user.first_name
        user_name = message.from_user.first_name
        rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

        query = ''
        for i in message.command[1:]:
            query += ' ' + str(i)
        print(query)
        await lel.edit("🎵 **Processing** sounds...")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            #print(results)
            title = results[0]["title"][:40]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            lel.edit(
                "❌ Song not found.\n\nTry another song or maybe spell it properly."
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [   
                [
                    InlineKeyboardButton(
                        text="ɪɴꜱᴛᴀɢʀᴀᴍ",
                        url=f"https://www.instagram.com/hendraputraaaaaa"),
                    InlineKeyboardButton(
                        text="ɢʀᴏᴜᴘ ᴍᴜꜱɪᴄ",
                        url=f"https://t.me/vcgsupportgroup"),
                
            ]                            
            ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(youtube.download(url))

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        qeue = que.get(message.chat.id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
        photo="final.png", 
        caption=f"🏷 **Judul:** [{title[:60]}]({url})\n⏱ **Durasi:** {duration}\n" \
               + f"💡 **Status:** Antrian ke {position}\n🎧 **Permintaan:** {requested_by}",
        reply_markup=keyboard)
        os.remove("final.png")
        return await lel.delete()
    else:
        chat_id = message.chat.id
        que[chat_id] = []
        qeue = que.get(message.chat.id)
        s_name = title            
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]      
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo="final.png",
        reply_markup=keyboard,
        caption=f"🏷 **Judul:** [{title[:60]}]({url})\n⏱ **Durasi:** {duration}\n" \
               + f"💡 **Status:** Playing\n🎧 **Permintaan:** {requested_by}"
        ),

        os.remove("final.png")
        return await lel.delete()


@Client.on_message(
    filters.command("dplay")
    & filters.group
    & ~ filters.edited
)
async def deezer(client: Client, message_: Message):
    global que
    lel = await message_.reply("🔄 Processing...")
    administrators = await get_administrators(message_.chat)
    chid = message_.chat.id
    try:
        user = await USER.get_me()
    except:
        user.first_name =  "Irama_Musik"
    usar = user
    wew = usar.id
    try:
        #chatdetails = await USER.get_chat(chid)
        lmoa = await client.get_chat_member(chid,wew)
    except:
           for administrator in administrators:
                      if administrator == message_.from_user.id:  
                          try:
                              invitelink = await client.export_chat_invite_link(chid)
                          except:
                              await lel.edit(
                                  "#Jadikan saya admin terlebih dahulu**",
                              )
                              return

                          try:
                              await USER.join_chat(invitelink)
                              await USER.send_message(message_.chat.id,"**Saya bergabung kesini didedikasi untuk memutar/mendownload lagu dan musik**")
                              await lel.edit(
                                  "**@Irama_Musik bergabung ke grup**",
                              )

                          except UserAlreadyParticipant:
                              pass
                          except Exception as e:
                              #print(e)
                              await lel.edit(
                                  f"**#Maaf @Irama_Musik tidak dapat bergabung, Pastikan dia tidak dibanned**"
                                   "\n\n**Atau add @Irama_Musik secara manual dengan tambahkan anggota!**",
                              )
                              pass
    try:
        chatdetails = await USER.get_chat(chid)
        #lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"**#Masukkan @Irama_Musik terlebih dahulu**"
        )
        return                            
    requested_by = message_.from_user.first_name   

    text = message_.text.split(" ", 1)
    queryy = text[1]
    res = lel
    await res.edit(f"Mencari Untuk **{queryy}** Via Deezer")
    try:
        arq = ARQ("https://thearq.tech")
        r = await arq.deezer(query=queryy, limit=1)
        title = r[0]["title"]
        duration = int(r[0]["duration"])
        thumbnail = r[0]["thumbnail"]
        artist = r[0]["artist"]
        url = r[0]["url"]
    except:
        await res.edit(
            "#Tidak Ditemukan Apapun!"
        )
        is_playing = False
        return
    keyboard = InlineKeyboardMarkup(
            [   
                [
                    InlineKeyboardButton(
                        text="ɪɴꜱᴛᴀɢʀᴀᴍ",
                        url=f"https://www.instagram.com/hendraputraaaaaa"),
                    InlineKeyboardButton(
                        text="ɢʀᴏᴜᴘ ᴍᴜꜱɪᴄ",
                        url=f"https://t.me/vcgsupportgroup"),
                
            ]                            
            ]
        )
    file_path= await converter.convert(wget.download(url))
    await res.edit("Generating Thumbnail")
    await generate_cover(requested_by, title, artist, duration, thumbnail)
    if message_.chat.id in callsmusic.pytgcalls.active_calls:
        await res.edit("adding in queue")
        position = await queues.put(message_.chat.id, file=file_path)       
        qeue = que.get(message_.chat.id)
        s_name = title
        r_by = message_.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await res.edit_text(f"**IramaMusik**= #️⃣ Queued at position {position}")
    else:
        await res.edit_text("Playing...")
        chat_id = message_.chat.id
        que[chat_id] = []
        qeue = que.get(message_.chat.id)
        s_name = title
        r_by = message_.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(message_.chat.id, file_path)

    await res.delete()

    m = await client.send_photo(
        chat_id=message_.chat.id,
        reply_markup=keyboard,
        photo="final.png",
        caption=f"🏷 **Judul:** [{title[:60]}]({url})\n⏱ **Durasi:** {duration}\n" \
               + f"💡 **Status:** `Playing`\n🎧 **Permintaan:** {requested_by}"
        ),
    os.remove("final.png")

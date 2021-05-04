from asyncio.queues import QueueEmpty
from cache.admins import set
from pyrogram import Client
from pyrogram.types import Message
from callsmusic import callsmusic
import traceback
import os
import sys
import sira
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram import filters, emoji
from config import BOT_NAME as BN
from helpers.filters import command, other_filters
from helpers.decorators import errors
from config import que, admins as a

@Client.on_message(filters.command('reload'))
async def update_admin(client, message):
    global a
    admins = await client.get_chat_members(message.chat.id, filter="administrators")
    new_ads = []
    for u in admins:
        new_ads.append(u.user.id)
    a[message.chat.id] = new_ads
    #await message.reply_text('Sucessfully updated admin list in **{}**'.format(message.chat.title))




@Client.on_message(command("pause") & other_filters)
@errors
async def pause(_, message: Message):
    callsmusic.pytgcalls.pause_stream(message.chat.id)
    await message.reply_text("▶️ Musik dijeda!")


@Client.on_message(command("resume") & other_filters)
@errors
async def resume(_, message: Message):
    callsmusic.pytgcalls.resume_stream(message.chat.id)
    await message.reply_text("⏸ Musik dilanjutkan!")


@Client.on_message(command("end") & other_filters)
@errors
async def stop(_, message: Message):
    try:
        callsmusic.queues.clear(message.chat.id)
    except:
        pass

    callsmusic.pytgcalls.leave_group_call(message.chat.id)
    await message.reply_text("⏹ Musik dihentikan!")


@Client.on_message(command("skip") & other_filters)
@errors
async def skip(_, message: Message):
    chat_id = message.chat.id

    sira.task_done(chat_id)
    await message.reply_text("⏭ Memproses...")
    if callsmusic.queues.is_empty(message.chat.id):
        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("Tidak ada musik dalam antrian")
    else:
        callsmusic.pytgcalls.change_stream(
                message.chat.id,
                callsmusic.queues.get(message.chat.id)["file"]
            )

        await message.reply_text("🔂 Melanjutkan ke lagu berikutnya!")

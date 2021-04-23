from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn

@Client.on_message(filters.command("start") & filters.private & ~filters.channel)
async def start(_, message: Message):
    await message.reply_text(
        f"""<b>👋🏻 Hai {message.from_user.first_name}!</b>

Aku adalah Irama Musik Bot, bot sumber terbuka yang memungkinkan Anda memutar musik di grup telegram Anda.
Tidak mengetahui cara memakainya? Baca panduan pemakaian agar langsung memahami tanpa bertanya!
━━━━━━━━━━━━━━━━━━━━━━
Bot : @IramaMusikBot - Asisten : @Irama_Musik
Dikelola oleh 🌻 [Hendra](t.me/IamYourEnemy). Thanks! 
        """,
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "📒 Panduan Pemakaian", url="https://telegra.ph/IIrama-Musik-04-22")
                  ],[
                    InlineKeyboardButton(
                        "📊 Channel Support", url="https://t.me/AkuUserBot"
                    ),
                    InlineKeyboardButton(
                        "🔉 Channel Bucin", url="https://t.me/kutipankataaa") 
                  ],[
                    InlineKeyboardButton(
                        "📈 Group Support", url="https://t.me/VcgSupportGroup"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )

@Client.on_message(filters.command("reload") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
      await message.reply_text("""**🎧 Pemutar Musik Sedang Online**""",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Group Support", url="https://t.me/VcgSupportGroup"
                    ),
                    InlineKeyboardButton(
                        "Owner Bot", url="https://t.me/IamYourEnemy"
                    )
                ]
            ]
        )
   )

@Client.on_message(filters.command("start") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
      await message.reply_text("""**🎧 Pemutar Musik Sedang Online**""",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⚡ Pemilik ⚡", url="https://t.me/VcgSupportGroup") 
                ],[
                    InlineKeyboardButton(
                        "Group Support", url="https://t.me/VcgSupportGroup"
                    )
                ]
            ]
        )
   )

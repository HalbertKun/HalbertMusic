from callsmusic.callsmusic import client as USER
from pyrogram import filters
from pyrogram.types import Chat, Message, User


@USER.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmPermit(client: USER, message: Message):
  await USER.send_message(message.chat.id,"Alooo Ges 🤩 Saya adalah **Layanan Asisten Irama Musik Bot.**\n\n ❗️ Rules :\n   - Biasakan salam, amanat dari [Owner](t.me/IamYourEnemy) \n   - Jangan spam pemutaran lagu agar bot tidak error \n\n **Note :** Kirim link undangan grup atau username grup jika userbot/asisten tidak dapat bergabung dengan grup anda atau yang lainnya.\n\n 🛠️ Ke [Group Support](t.me/VcgSupportGroup) atau bisa PC ke owner [Hendra](t.me/IamYourEnemy)\n\n")
  return                        

import config, asyncio
from bot import Bot
from pyrogram import types, filters
from databases import userbase
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked

@Bot.on_message(filters.command('start') & (filters.private | filters.group))
async def startMessage(client: Bot, msg:types.Message):
    if not await userbase.getUser(msg.from_user.id):
        namaLengkap = msg.from_user.first_name if not msg.from_user.last_name else msg.from_user.first_name
        await userbase.addUser(msg.from_user.id, namaLengkap)
    await msg.reply_photo(
        photo=config.IMG_START,
        caption=config.IMG_CAPTION.format(
            id=msg.from_user.id,
            first=msg.from_user.first_name,
            last=msg.from_user.last_name,
            username=msg.from_user.username,
            dc_id=msg.from_user.dc_id,
            lang=msg.from_user.language_code,
            type=msg.chat.type.value,
            mention=msg.from_user.mention
        ), 
        reply_markup=types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton('CHANNEL', url=await client.export_chat_invite_link(config.CHANNEL_ID))]
        ])
    )

@Bot.on_message(filters.command('help') & (filters.private | filters.group))
async def helpMessage(_, msg:types.Message):
    await msg.reply("""𝗝𝘂𝘀𝘁 𝗜𝗻𝗳𝗼 𝗨𝗻𝘁𝘂𝗸 𝗨𝘀𝗲𝗿:
• Silahkan pilih dan kirim konten yang ingin kalian Donate
• Tunggu sampai Admin Online, Chat kalian pasti akan dibalas
𝗨𝗻𝘁𝘂𝗸 𝗔𝗱𝗺𝗶𝗻:
•/users - memblokir anak dajjal
•/broadcast - memblokir anak dajjal
•/ban <alasan> - memblokir anak dajjal
•/unban - membuka blokir anak haram
𝗡𝗼𝘁𝗲:<code> Jangan melakukan spam Chat jika tidak ingin diban</code>
"""	
)

@Bot.on_message(filters.command('users') & (filters.private | filters.group))
async def usersMessage(_, msg: types.Message):
    if msg.from_user.id == config.OWNER_ID:
        users = await userbase.getAll()
        await msg.reply(f'<b>Total users dibot ini adalah {len(users)} users</b>')
    else:
        await msg.reply('<b>Anda tidak memiliki akses!</b>')

@Bot.on_message(filters.command('broadcast') & (filters.private | filters.group))
async def broadcastMessage(client, msg: types.Message):
    if msg.from_user.id == config.OWNER_ID:
        if msg.reply_to_message:
            users = await userbase.getAll()
            broadcast_msg = msg.reply_to_message
            total = 0
            successful = 0
            blocked = 0
            deleted = 0
            unsuccessful = 0
            batas = 1000
            pls_wait = await msg.reply(
                "<code>Broadcasting Message Tunggu Sebentar...</code>"
            )
            for chat_id in users:
                try:
                    if broadcast_msg.text:
                        await client.send_message(chat_id, f"<b>🔔BROADCAST</b>\n\n{broadcast_msg.text}")
                        successful += 1
                    else:
                        await broadcast_msg.copy(chat_id, caption=f"<b>🔔BROADCAST</b>\n\n{broadcast_msg.caption}") 
                        successful += 1
                except FloodWait as e:
                    if broadcast_msg.text:
                        await asyncio.sleep(e.x)
                        await client.send_message(chat_id, f"<b>🔔BROADCAST</b>\n\n{broadcast_msg.text}")
                        successful += 1
                    else:
                        await asyncio.sleep(e.x)
                        await broadcast_msg.copy(chat_id, caption=f"<b>🔔BROADCAST</b>\n\n{broadcast_msg.caption}")
                        successful += 1
                except UserIsBlocked:
                    blocked += 1
                except InputUserDeactivated:
                    deleted += 1
                except BaseException:
                    unsuccessful += 1
                total += 1
                if total == batas:
                    batas += 1000
                    status = f"""<b><u>Proses Broadcast Masih Berlangsung</u>
Jumlah Pengguna: <code>{total}</code>
Berhasil: <code>{successful}</code>
Gagal: <code>{unsuccessful}</code>
Pengguna diblokir: <code>{blocked}</code>
Akun Terhapus: <code>{deleted}</code></b>\n\nBroadcast sedang berlangung, tunggu sebentar..."""
                        # BATAS
                    await pls_wait.edit(status)
            status = f"""<b><u>Berhasil Broadcast</u>
Jumlah Pengguna: <code>{total}</code>
Berhasil: <code>{successful}</code>
Gagal: <code>{unsuccessful}</code>
Pengguna diblokir: <code>{blocked}</code>
Akun Terhapus: <code>{deleted}</code></b>"""
            await pls_wait.delete()
            return await msg.reply(status)
        else:
            await msg.reply('<b>untuk melakukan broadcast, silahkan reply pesan!</b>')
    else:
        await msg.reply('<b>Anda tidak memiliki akses!</b>')
import config
from pyrogram import filters, types
from databases import userbase, chat
from bot import Bot

@Bot.on_message(filters.command('ban') & (filters.private | filters.group))
async def banMessage(_, msg: types.Message):
    if msg.from_user.id == config.OWNER_ID:
        if msg.reply_to_message:
            data = await chat.getMessage(msg.reply_to_message.id)
            if data:
                from_id = data['from_user']
                if len(msg.command) == 1:
                    uid = from_id
                    alasan = "Tidak ada alasan"
                else:
                    uid = from_id
                    alasan = msg.text.split(None, 1)[1]
                if msg.reply_to_message.from_user.id == from_id:
                    return await msg.reply("Tidak dapat menggunakan id sendiri")            
                user = await userbase.getUser(uid)
                if user:
                    await userbase.updateBan(uid, "ban", alasan)    
                    await msg.reply(f'[ <code>{user["_id"]}</code> ] - [ <code>{user["namaLengkap"]}</code> ] behasil di ban dengan alasan : {alasan}')
                else:
                    await msg.reply(f"[ <code>{uid}</code> ] ID Tidak ada didatabase nih")
            else:
                await msg.reply(f"[ <code>{msg.reply_to_message.id}</code> ] MESSAGE ID Tidak ada didatabase nih")
        else:
            await msg.reply("Reply Pesan Forward\n\n<code>/ban [Alasan]</code>")
    else:            
        await msg.reply("<b>Anda tidak ada hak untuk menggunakan perintah ini!</b>")

@Bot.on_message(filters.command('unban') & (filters.private | filters.group))
async def unbanMessage(_, msg: types.Message):
    if msg.from_user.id == config.OWNER_ID:
        if msg.reply_to_message:
            if msg.reply_to_message.from_user.id == msg.from_user.id:
                return await msg.reply("Tidak dapat menggunakan id sendiri") 
            data = await chat.getMessage(msg.reply_to_message.id)
            if data:
                uid = data['from_user']
                alasan = "Tidak ada alasan"
                user = await userbase.getUser(uid)
                if user:
                    if user['status'] != 'ban':
                        return await msg.reply(f'[ <code>{user["_id"]}</code> ] - [ <code>{user["namaLengkap"]}</code> ] tidak sedang dalam kondisi ban')
                    await userbase.updateBan(uid, "member", alasan)    
                    await msg.reply(f'[ <code>{user["_id"]}</code> ] - [ <code>{user["namaLengkap"]}</code> ] behasil diunban')
                else:
                    await msg.reply(f"[ <code>{uid}</code> ] ID Tidak ada didatabase nih")
            else:
                await msg.reply(f"[ <code>{msg.reply_to_message.id}</code> ] MESSAGE ID Tidak ada didatabase nih")
        else:
            if len(msg.command) != 1:
                uid = msg.text.split(' ')[1]
                alasan = "Tidak ada alasan"
                user = await userbase.getUser(int(uid))
                if user:
                    if user['status'] != 'ban':
                        return await msg.reply(f'[ <code>{user["_id"]}</code> ] - [ <code>{user["namaLengkap"]}</code> ] tidak sedang dalam kondisi ban')
                    await userbase.updateBan(uid, "member", alasan)    
                    await msg.reply(f'[ <code>{user["_id"]}</code> ] - [ <code>{user["namaLengkap"]}</code> ] behasil diunban')
                else:
                    await msg.reply(f"[ <code>{uid}</code> ] ID Tidak ada didatabase nih")
            else:
                await msg.reply("Reply Pesan Forward untuk ban\nAtau /ban [id]")
    else:            
        await msg.reply("<b>Anda tidak ada hak untuk menggunakan perintah ini!</b>")
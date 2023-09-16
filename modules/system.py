# Copyright (C) 2020 - Dragon Userbot

from time import perf_counter

from pyrogram import(
    Client,
    filters
)
from pyrogram.types import Message

from utils.format import format_exc
from utils.database import db, prefix
from utils.helpers.updater import(
    uppip,
    gpull,
    upreq,
    restart,
    DESC
)


@Client.on_message(filters.command("about", prefix) & filters.me)
async def _about(client: Client, message: Message):
    await message.edit("...")
    await message.reply_photo(
        "assets/dragon.png",
        caption=DESC
    )
    await message.delete()


@Client.on_message(filters.command("ping", prefix) & filters.me)
async def _ping(_, message: Message):
    start = perf_counter()
    await message.edit("...")
    end = perf_counter()
    elapsed = round((end - start) * 1000, 3)
    await message.edit(f"Result: {elapsed}ms")


@Client.on_message(filters.command("restart", prefix) & filters.me)
async def _restart(_, message: Message):
    db.set(
        "core.updater",
        "restart_info",
        {
            "type": "restart",
            "chat_id": message.chat.id,
            "message_id": message.id,
        },
    )
    await message.edit("Restarting...")
    restart()


@Client.on_message(filters.command("update", prefix) & filters.me)
async def _update(_, message: Message):
    db.set(
        "core.updater",
        "restart_info",
        {
            "type": "update",
            "chat_id": message.chat.id,
            "message_id": message.id,
        },
    )
    await message.edit("Updating...")
    
    try:
        uppip()
        gpull()
        upreq()
    except Exception as e:
        await message.edit(format_exc(e))
        db.remove("core.updater", "restart_info")
    else:
        await message.edit("Restarting...")
        restart()

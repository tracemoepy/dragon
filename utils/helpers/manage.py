from typing import Union

from pyrogram import Client, types
from pyrogram.utils import(
    MIN_CHAT_ID,
    MAX_USER_ID,
    MIN_CHANNEL_ID,
    MAX_CHANNEL_ID
)

from utils.database import db


async def _user(message: types.Message):
    if message.reply_to_message.from_user:
        return (
            message.reply_to_message.from_user.id,
            message.reply_to_message.from_user.first_name,
        )
    elif message.reply_to_message.sender_chat:
        return (
            message.reply_to_message.sender_chat.id,
            message.reply_to_message.sender_chat.title,
        )


async def _check(data: Union[str, int]) -> str:
    data = str(data)
    if (
        not data.isdigit()
        and data[0] == "-"
        and not data[1:].isdigit()
        or not data.isdigit()
        and data[0] != "-"
    ):
        return "channel"
    else:
        peer_id = int(data)
    if peer_id < 0:
        if MIN_CHAT_ID <= peer_id:
            return "chat"

        if MIN_CHANNEL_ID <= peer_id < MAX_CHANNEL_ID:
            return "channel"
    elif 0 < peer_id <= MAX_USER_ID:
        return "user"

    raise ValueError(f"Peer id invalid: {peer_id}")


def _reply(func):
    async def wrapped(client: Client, message: types.Message):
        if not message.reply_to_message:
            await message.edit("Reply to message is required!")
        else:
            return await func(client, message)

    return wrapped


def _text(message: types.Message) -> str:
    return message.text if message.text else message.caption


db_cache: dict = db.get_collection("core.ats")


def _cache():
    db_cache.clear()
    db_cache.update(db.get_collection("core.ats"))

import asyncio

from pyrogram import Client
from pyrogram.types import Message

async def purge(
    client: Client,
    message: Message,
    start: int = 0,
    end: int = 0,
    type: str = "all",
    count: int = 0,
) -> None:
    count_deleted = 0
    index = 0
    while (count_deleted < count) if not count == 0 else (start + index < end):
        try:
            msg = await client.get_messages(
                chat_id=message.chat.id,
                message_ids=(start - index)
                if not count == 0 else (
                    start + index
                ),
                replies=0,
            )
            if msg:
                if type == "me":
                    if not msg.from_user.id == message.from_user.id:
                        index += 1
                        continue
                if await msg.delete():
                    count_deleted += 1
        except:
            pass
        index += 1
    if count_deleted > 0:
        msg = await message.reply(
            text=f"{count_deleted} "
                 "messages are purged"
        )
        await asyncio.sleep(1)
        await msg.delete()
    return [True, count_deleted]

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.database import prefix
from utils.helpers.purge import purge
from utils.helpers.filters import supports


@Client.on_message(filters.command("del", prefix) & filters.me)
async def _del(client: Client, message: Message) -> None:
    await message.delete()
    if message.reply_to_message:
        try:
            msg = await client.get_messages(
                chat_id=message.chat.id,
                message_ids=message.reply_to_message.id,
                replies=0
            )
            await msg.delete()
        except:
            pass


@Client.on_message(
    filters.command("purge", prefix) 
    & filters.me 
    & ~filters.user
    & ~filters.bot
    & ~supports
)
async def _purge(client: Client, message: Message) -> None:
    await message.delete()
    if message.reply_to_message:
        await purge(
            client,
            message,
            start=message.reply_to_message.id,
            end=message.id
        )


@Client.on_message(
    filters.command("purgeme", prefix)
    & filters.me 
    & ~filters.user
    & ~filters.bot
    & ~supports
)
async def _purgeme(client: Client, message: Message) -> None:
    await message.delete()
    count = int(
        message.command[1]
        ) if len(message.command) > 1 else 1
    await purge(
        client,
        message,
        start=message.id - 1,
        type="me",
        count=count
    )

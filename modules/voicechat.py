from asyncio import sleep
from random import randint

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall

from utils.format import format_exc
from utils.helpers.tgcalls import _calls
from utils.database import prefix


@Client.on_message(filters.command("vc", prefix) & filters.me)
async def _vc(client: Client, message: Message):
    chat_id = message.chat.id
    active = await _calls(client, message)
    if len(message.command) == 1:
        await message.edit(
            "Togle Voice Chat\n" \
            f"  Start: <code>{prefix}vc on</code>\n" \
            f"  Stop: <code>{prefix}vc off</code>"
        )
        return
    
    elif message.command[1] == "on":
        await message.edit("Starting...")
        try:
            if active:
                await message.edit(
                    "Voice chat already started!")
                await sleep(2)
                return await message.delete()
            else:
                await client.invoke(
                    CreateGroupCall(
                        peer=(
                            await client.resolve_peer(
                                chat_id
                            )
                        ),
                        random_id=randint(
                            -2147483648,
                            2147483647
                        )
                    )
                )
                await message.edit("Voice chat started!")
        except Exception as e:
            await message.edit(format_exc(e))
    elif message.command[1] == "off":
        await message.edit("Stoping...")
        try:
            if not active:
                await message.edit(
                    "Voice chat already stopped!")
                await sleep(2)
                return await message.delete()
            else:
                await client.invoke(
                    DiscardGroupCall(
                        call=active
                    )
                )
                await message.edit(
                    "Voice chat stopped!")
                await sleep(2)
                return await message.delete()
        except Exception as e:
            await message.edit(format_exc(e))


@Client.on_message(filters.command("join", prefix) & filters.me)
async def _join(client: Client, message: Message):
    chat_id = message.chat.id
    await message.edit("Joining...")
    try:
        await client._voicechat.start(chat_id)
        await message.edit(
            "Joined to voice chat!")
        await sleep(2)
        return await message.delete()
    except Exception as e:
        await message.edit(format_exc(e))
        
        
@Client.on_message(filters.command("leave", prefix) & filters.me)
async def _leave(client: Client, message: Message):
    await message.edit("Leaving...")
    try:
        await client._voicechat.stop()
        await message.edit(
            "Left from voice chat!")
        await sleep(2)
        return await message.delete()
    except Exception as e:
        await message.edit(format_exc(e))


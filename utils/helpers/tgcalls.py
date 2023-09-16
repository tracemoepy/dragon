from typing import Optional

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.raw.types import(
    InputGroupCall,
    InputPeerChat,
    InputPeerChannel
)
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.channels import GetFullChannel

from utils.format import format_exc


async def _calls(
    client: Client,
    message: Message, 
    e: str = ""
) -> Optional[InputGroupCall]:
    peer = await client.resolve_peer(message.chat.id)
    if isinstance(
        peer,
        (InputPeerChannel, InputPeerChat)
    ):
        if isinstance(peer, InputPeerChannel):
            full = (
                await client.invoke(GetFullChannel(channel=peer))
            ).full_chat
        elif isinstance(peer, InputPeerChat):
            full = (
                await client.invoke(GetFullChat(chat_id=peer.chat_id))
            ).full_chat
        if full is not None:
            return full.call
    await message.edit(f"{format_exc(e)}")
    return False


from pytgcalls import GroupCallFactory

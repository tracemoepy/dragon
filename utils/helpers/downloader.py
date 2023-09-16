import os

async def download(
    client,
    message,
    chatid,
    msgid
):
    msg = await client.get_messages(chatid, msgid)
    if "text" in str(msg):
        await client.send_message(
            message.chat.id,
            msg.text,
        )
        return await message.delete()
    file = await client.download_media(msg)
    if "Document" in str(msg):
        await client.send_document(
            message.chat.id,
            file,
            caption=msg.caption,
        )
    elif "Video" in str(msg):
        await client.send_video(
            message.chat.id,
            file,
            duration=msg.video.duration,
            width=msg.video.width,
            height=msg.video.height,
            caption=msg.caption,
        )
    elif "Animation" in str(msg):
        await client.send_animation(
            message.chat.id,
            file,
        )
    elif "Sticker" in str(msg):
        await client.send_sticker(
            message.chat.id,
            file,
        )
    elif "Voice" in str(msg):
        await client.send_voice(
            message.chat.id,
            file,
            caption=msg.caption,
        )
    elif "Audio" in str(msg):
        await client.send_audio(
            message.chat.id,
            file,
            caption=msg.caption,
        )   
    elif "Photo" in str(msg):
        await client.send_photo(
            message.chat.id,
            file,
            caption=msg.caption,
        )
    os.remove(file)
    await message.delete()
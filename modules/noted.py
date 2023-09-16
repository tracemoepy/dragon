#  Copyright (C) 2020 - Dragon Userbot

from pyrogram import Client, filters, errors
from pyrogram.types import (
    Message,
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaAudio,
    InputMediaDocument,
)

from utils.database import db, prefix


@Client.on_message(filters.command("save", prefix) & filters.me)
async def save_note(client: Client, message: Message):
    await message.edit("Loading...")

    try:
        chat = await client.get_chat(db.get("core.notes", "chat_id", 0))
    except (errors.RPCError, ValueError, KeyError):
        chat = await client.create_supergroup(
            "Dragon-Fork Dump"
        )
        db.set("core.notes", "chat_id", chat.id)

    chat_id = chat.id

    if message.reply_to_message and len(message.text.split()) >= 2:
        note_name = message.text.split(maxsplit=1)[1]
        if message.reply_to_message.media_group_id:
            checking_note = db.get("core.notes", f"note{note_name}", False)
            if not checking_note:
                get_media_group = [
                    _.id
                    for _ in await client.get_media_group(
                        message.chat.id, message.reply_to_message.id
                    )
                ]
                try:
                    message_id = await client.forward_messages(
                        chat_id, message.chat.id, get_media_group
                    )
                except errors.ChatForwardsRestricted:
                    await message.edit(
                        "Forwarding messages is restricted by chat admins!"
                    )
                    return
                note = {
                    "MESSAGE_ID": str(message_id[1].id),
                    "MEDIA_GROUP": True,
                    "CHAT_ID": str(chat_id),
                }
                db.set("core.notes", f"note{note_name}", note)
                await message.edit(f"Note <code>{note_name}</code> saved!")
            else:
                await message.edit("This note already exists!")
        else:
            checking_note = db.get("core.notes", f"note{note_name}", False)
            if not checking_note:
                try:
                    message_id = await message.reply_to_message.forward(chat_id)
                except errors.ChatForwardsRestricted:
                    message_id = await message.copy(chat_id)
                note = {
                    "MEDIA_GROUP": False,
                    "MESSAGE_ID": str(message_id.id),
                    "CHAT_ID": str(chat_id),
                }
                db.set("core.notes", f"note{note_name}", note)
                await message.edit(f"Note <code>{note_name}</code> saved!")
            else:
                await message.edit("This note already exists!")
    elif len(message.text.split()) >= 3:
        note_name = message.text.split(maxsplit=1)[1].split()[0]
        checking_note = db.get("core.notes", f"note{note_name}", False)
        if not checking_note:
            message_id = await client.send_message(
                chat_id, message.text.split(note_name)[1].strip()
            )
            note = {
                "MEDIA_GROUP": False,
                "MESSAGE_ID": str(message_id.id),
                "CHAT_ID": str(chat_id),
            }
            db.set("core.notes", f"note{note_name}", note)
            await message.edit(f"Note {note_name} saved!")
        else:
            await message.edit("This note already exists!")
    else:
        await message.edit(
            f"Example: <code>{prefix}save </code> [name]"
        )


@Client.on_message(filters.command("get", prefix) & filters.me)
async def note_send(client: Client, message: Message):
    if len(message.text.split()) >= 2:
        await message.edit("Loading...")

        note_name = f"{message.text.split(maxsplit=1)[1]}"
        find_note = db.get("core.notes", f"note{note_name}", False)
        if find_note:
            try:
                await client.get_messages(
                    int(find_note["CHAT_ID"]), int(find_note["MESSAGE_ID"])
                )
            except errors.RPCError:
                await message.edit(
                    "Sorry, but this note is unavaliable.\n"
                    f"You can delete this note with "
                    f"<code>{prefix}clear {note_name}</code>"
                )
                return

            if find_note.get("MEDIA_GROUP"):
                messages_grouped = await client.get_media_group(
                    int(find_note["CHAT_ID"]), int(find_note["MESSAGE_ID"])
                )
                media_grouped_list = []
                for _ in messages_grouped:
                    if _.photo:
                        if _.caption:
                            media_grouped_list.append(
                                InputMediaPhoto(
                                    _.photo.file_id, _.caption.markdown
                                )
                            )
                        else:
                            media_grouped_list.append(
                                InputMediaPhoto(_.photo.file_id)
                            )
                    elif _.video:
                        if _.caption:
                            if _.video.thumbs:
                                media_grouped_list.append(
                                    InputMediaVideo(
                                        _.video.file_id,
                                        _.video.thumbs[0].file_id,
                                        _.caption.markdown,
                                    )
                                )
                            else:
                                media_grouped_list.append(
                                    InputMediaVideo(
                                        _.video.file_id, _.caption.markdown
                                    )
                                )
                        elif _.video.thumbs:
                            media_grouped_list.append(
                                InputMediaVideo(
                                    _.video.file_id, _.video.thumbs[0].file_id
                                )
                            )
                        else:
                            media_grouped_list.append(
                                InputMediaVideo(_.video.file_id)
                            )
                    elif _.audio:
                        if _.caption:
                            media_grouped_list.append(
                                InputMediaAudio(
                                    _.audio.file_id, _.caption.markdown
                                )
                            )
                        else:
                            media_grouped_list.append(
                                InputMediaAudio(_.audio.file_id)
                            )
                    elif _.document:
                        if _.caption:
                            if _.document.thumbs:
                                media_grouped_list.append(
                                    InputMediaDocument(
                                        _.document.file_id,
                                        _.document.thumbs[0].file_id,
                                        _.caption.markdown,
                                    )
                                )
                            else:
                                media_grouped_list.append(
                                    InputMediaDocument(
                                        _.document.file_id, _.caption.markdown
                                    )
                                )
                        elif _.document.thumbs:
                            media_grouped_list.append(
                                InputMediaDocument(
                                    _.document.file_id,
                                    _.document.thumbs[0].file_id,
                                )
                            )
                        else:
                            media_grouped_list.append(
                                InputMediaDocument(_.document.file_id)
                            )
                if message.reply_to_message:
                    await client.send_media_group(
                        message.chat.id,
                        media_grouped_list,
                        reply_to_message_id=message.reply_to_message.id,
                    )
                else:
                    await client.send_media_group(
                        message.chat.id, media_grouped_list
                    )
            elif message.reply_to_message:
                await client.copy_message(
                    message.chat.id,
                    int(find_note["CHAT_ID"]),
                    int(find_note["MESSAGE_ID"]),
                    reply_to_message_id=message.reply_to_message.id,
                )
            else:
                await client.copy_message(
                    message.chat.id,
                    int(find_note["CHAT_ID"]),
                    int(find_note["MESSAGE_ID"]),
                )
            await message.delete()
        else:
            await message.edit("There is no such note!")
    else:
        await message.edit(
            f"Example: <code>{prefix}get </code> [name]"
        )


@Client.on_message(filters.command("notes", prefix) & filters.me)
async def notes(_, message: Message):
    await message.edit("Loading...")
    text = "Available Notes:\n"
    collection = db.get_collection("core.notes")
    for note in collection.keys():
        if note[:4] == "note":
            text += f"  <code>{note[4:]}</code>\n"
    await message.edit(text)


@Client.on_message(filters.command(["clear"], prefix) & filters.me)
async def clear_note(_, message: Message):
    if len(message.text.split()) >= 2:
        note_name = message.text.split(maxsplit=1)[1]
        find_note = db.get("core.notes", f"note{note_name}", False)
        if find_note:
            db.remove("core.notes", f"note{note_name}")
            await message.edit(f"Note <code>{note_name}</code> deleted!")
        else:
            await message.edit("There is no such note!")
    else:
        await message.edit(
            f"Example: <code>{prefix}clear [name]</code>"
        )

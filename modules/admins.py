#  Copyright (C) 2020 - Dragon Userbot

import re

from time import time
from typing import Dict
from datetime import timedelta, datetime
from contextlib import suppress

from pyrogram.raw import functions, types
from pyrogram import(
    Client,
    ContinuePropagation,
    filters
)
from pyrogram.errors import (
    UserAdminInvalid,
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameInvalid,
    RPCError,
)
from pyrogram.types import(
    Message,
    ChatPermissions,
    ChatPrivileges
)
from pyrogram.utils import get_channel_id

from utils.database import db, prefix
from utils.format import format_exc
from utils.helpers.manage import(
    _text,
    _reply,
    _cache,
    _check,
    _user
)


db_cache: dict = db.get_collection("core.ats")


@Client.on_message(filters.group & ~filters.me)
async def _admins(_, message: Message):
    if message.sender_chat:
        if (
            message.sender_chat.type == "supergroup"
            or message.sender_chat.id
            == db_cache.get(f"linked{message.chat.id}", 0)
        ):
            raise ContinuePropagation

    if message.sender_chat and db_cache.get(f"antich{message.chat.id}", False):
        with suppress(RPCError):
            await message.delete()
            await message.chat.ban_member(message.sender_chat.id)

    raise ContinuePropagation


@Client.on_message(filters.command("ban", prefix) & filters.me)
async def _ban(client: Client, message: Message):
    cause = _text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        user_for_ban, name = await _user(message)
        try:
            await client.ban_chat_member(message.chat.id, user_for_ban)
            channel = await client.resolve_peer(message.chat.id)
            user_id = await client.resolve_peer(user_for_ban)
            if "rs" in cause.lower().split():
                await client.invoke(
                    functions.channels.ReportSpam(
                        channel=channel,
                        participant=user_id,
                        id=[message.reply_to_message.id],
                    )
                )
            if "dh" in cause.lower().split():
                await client.invoke(
                    functions.channels.DeleteParticipantHistory(
                        channel=channel, participant=user_id
                    )
                )
            _text_c = "".join(
                f" {_}"
                for _ in cause.split()
                if _.lower() not in ["dh", "rs"]
            )

            await message.edit(
                f"{name} banned!"
                + f"\n{'Reason: ' + _text_c.split(maxsplit=1)[1] + '' if len(_text_c.split()) > 1 else ''}"
            )
        except UserAdminInvalid:
            await message.edit("No rights!")
        except ChatAdminRequired:
            await message.edit("No rights!")
        except Exception as e:
            await message.edit(format_exc(e))
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                if await _check(cause.split(" ")[1]) == "channel":
                    user_to_ban = await client.get_chat(cause.split(" ")[1])
                elif await _check(cause.split(" ")[1]) == "user":
                    user_to_ban = await client.get_users(cause.split(" ")[1])
                else:
                    await message.edit("Invalid user type!")
                    return

                name = (
                    user_to_ban.first_name
                    if getattr(user_to_ban, "first_name", None)
                    else user_to_ban.title
                )

                try:
                    channel = await client.resolve_peer(message.chat.id)
                    user_id = await client.resolve_peer(user_to_ban.id)
                    if (
                        "rs" in cause.lower().split()
                        and message.reply_to_message
                    ):
                        await client.invoke(
                            functions.channels.ReportSpam(
                                channel=channel,
                                participant=user_id,
                                id=[message.reply_to_message.id],
                            )
                        )
                    if "dh" in cause.lower().split():
                        await client.invoke(
                            functions.channels.DeleteParticipantHistory(
                                channel=channel, participant=user_id
                            )
                        )

                    _text_c = "".join(
                        f" {_}"
                        for _ in cause.split()
                        if _.lower() not in ["dh", "rs"]
                    )

                    await client.ban_chat_member(
                        message.chat.id, user_to_ban.id
                    )
                    await message.edit(
                        f"{name} banned!"
                        + f"\n{'Reason: ' + _text_c.split(' ', maxsplit=2)[2] + '' if len(_text_c.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("No rights!")
                except ChatAdminRequired:
                    await message.edit("No rights!")
                except Exception as e:
                    await message.edit(format_exc(e))
            except PeerIdInvalid:
                await message.edit("User is not found!")
            except UsernameInvalid:
                await message.edit("User is not found!")
            except IndexError:
                await message.edit("User is not found!")
        else:
            await message.edit("user_id or username!")
    else:
        await message.edit("Unsupported!")


@Client.on_message(filters.command("unban", prefix) & filters.me)
async def _unban(client: Client, message: Message):
    cause = _text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        user_for_unban, name = await _user(message)
        try:
            await client.unban_chat_member(message.chat.id, user_for_unban)
            await message.edit(
                f"{name} unbanned!"
                + f"\n{'Reason: ' + cause.split(maxsplit=1)[1] + '' if len(cause.split()) > 1 else ''}"
            )
        except UserAdminInvalid:
            await message.edit("No rights!")
        except ChatAdminRequired:
            await message.edit("No rights!")
        except Exception as e:
            await message.edit(format_exc(e))

    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                if await _check(cause.split(" ")[1]) == "channel":
                    user_to_unban = await client.get_chat(cause.split(" ")[1])
                elif await _check(cause.split(" ")[1]) == "user":
                    user_to_unban = await client.get_users(cause.split(" ")[1])
                else:
                    await message.edit("Invalid user type!")
                    return

                name = (
                    user_to_unban.first_name
                    if getattr(user_to_unban, "first_name", None)
                    else user_to_unban.title
                )

                try:
                    await client.unban_chat_member(
                        message.chat.id, user_to_unban.id
                    )
                    await message.edit(
                        f"{name} unbanned!"
                        + f"\n{'Reason: ' + cause.split(' ', maxsplit=2)[2] + '' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("No rights!")
                except ChatAdminRequired:
                    await message.edit("No rights!")
                except Exception as e:
                    await message.edit(format_exc(e))
            except PeerIdInvalid:
                await message.edit("User is not found!")
            except UsernameInvalid:
                await message.edit("User is not found!")
            except IndexError:
                await message.edit("User is not found!")
        else:
            await message.edit("user_id or username!")
    else:
        await message.edit("Unsupported!")


@Client.on_message(filters.command("kick", prefix) & filters.me)
async def _kick(client: Client, message: Message):
    cause = _text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if message.reply_to_message.from_user:
            try:
                await client.ban_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    datetime.now() + timedelta(minutes=1),
                )
                channel = await client.resolve_peer(message.chat.id)
                user_id = await client.resolve_peer(
                    message.reply_to_message.from_user.id
                )
                if (
                    "rs" in cause.lower().split()
                    and message.reply_to_message
                ):
                    await client.invoke(
                        functions.channels.ReportSpam(
                            channel=channel,
                            participant=user_id,
                            id=[message.reply_to_message.id],
                        )
                    )
                if "dh" in cause.lower().split():
                    await client.invoke(
                        functions.channels.DeleteParticipantHistory(
                            channel=channel, participant=user_id
                        )
                    )
                _text_c = "".join(
                    f" {_}"
                    for _ in cause.split()
                    if _.lower() not in ["dh", "rs"]
                )

                await message.edit(
                    f"{message.reply_to_message.from_user.first_name} kicked!"
                    + f"\n{'Reason: ' + _text_c.split(maxsplit=1)[1] + '' if len(_text_c.split()) > 1 else ''}"
                )
            except UserAdminInvalid:
                await message.edit("No rights!")
            except ChatAdminRequired:
                await message.edit("No rights!")
            except Exception as e:
                await message.edit(format_exc(e))
        else:
            await message.edit("Reply on user message!")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                user_to_ban = await client.get_users(cause.split(" ")[1])
                try:
                    channel = await client.resolve_peer(message.chat.id)
                    user_id = await client.resolve_peer(user_to_ban.id)
                    if (
                        "rs" in cause.lower().split()
                        and message.reply_to_message
                    ):
                        await client.invoke(
                            functions.channels.ReportSpam(
                                channel=channel,
                                participant=user_id,
                                id=[message.reply_to_message.id],
                            )
                        )
                    if "dh" in cause.lower().split():
                        await client.invoke(
                            functions.channels.DeleteParticipantHistory(
                                channel=channel, participant=user_id
                            )
                        )

                    _text_c = "".join(
                        f" {_}"
                        for _ in cause.split()
                        if _.lower() not in ["dh", "rs"]
                    )

                    await client.ban_chat_member(
                        message.chat.id,
                        user_to_ban.id,
                        datetime.now() + timedelta(minutes=1),
                    )
                    await message.edit(
                        f"{user_to_ban.first_name} kicked!"
                        + f"\n{'Reason: ' + _text_c.split(' ', maxsplit=2)[2] + '' if len(_text_c.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("No rights!")
                except ChatAdminRequired:
                    await message.edit("No rights!")
                except Exception as e:
                    await message.edit(format_exc(e))
            except PeerIdInvalid:
                await message.edit("User is not found!")
            except UsernameInvalid:
                await message.edit("User is not found!")
            except IndexError:
                await message.edit("User is not found!")
        else:
            await message.edit("user_id or username!")
    else:
        await message.edit("Unsupported!")


@Client.on_message(filters.command("zombie", prefix) & filters.me)
async def _zombie(client: Client, message: Message):
    await message.edit("Kicking deleted accounts...")
    try:
        values = [
            await message.chat.ban_member(
                member.user.id, datetime.now() + timedelta(seconds=31)
            )
            async for member in client.get_chat_members(message.chat.id)
            if member.user.is_deleted
        ]
    except Exception as e:
        return await message.edit(format_exc(e))
    await message.edit(
        f"Successfully kicked {len(values)} deleted account(s)!"
    )


@Client.on_message(filters.command("unmute", prefix) & filters.me)
async def _unmute(client, message):
    cause = _text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        u_p = message.chat.permissions
        if message.reply_to_message.from_user:
            try:
                await client.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    u_p,
                    datetime.now() + timedelta(seconds=30),
                )
                await message.edit(
                    f"{message.reply_to_message.from_user.first_name} unmuted!"
                    + f"\n{'Reason: ' + cause.split(' ', maxsplit=1)[1] + '' if len(cause.split()) > 1 else ''}"
                )
            except UserAdminInvalid:
                await message.edit("No rights!")
            except ChatAdminRequired:
                await message.edit("No rights!")
            except Exception as e:
                await message.edit(format_exc(e))
        else:
            await message.edit("Reply on user message!")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        u_p = message.chat.permissions
        if len(cause.split()) > 1:
            try:
                user_to_unmute = await client.get_users(cause.split(" ")[1])
                try:
                    await client.restrict_chat_member(
                        message.chat.id,
                        user_to_unmute.id,
                        u_p,
                        datetime.now() + timedelta(seconds=30),
                    )
                    await message.edit(
                        f"{user_to_unmute.first_name} unmuted!"
                        + f"\n{'Reason: ' + cause.split(' ', maxsplit=2)[2] + '' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("No rights!")
                except ChatAdminRequired:
                    await message.edit("No rights!")
                except Exception as e:
                    await message.edit(format_exc(e))
            except PeerIdInvalid:
                await message.edit("User is not found!")
            except UsernameInvalid:
                await message.edit("User is not found!")
            except IndexError:
                await message.edit("User is not found!")
        else:
            await message.edit("user_id or username!")
    else:
        await message.edit("Unsupported!")


@Client.on_message(filters.command("mute", prefix) & filters.me)
async def _mute(client: Client, message: Message):
    cause = _text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        mute_seconds: int = 0
        for character in "mhdw":
            match = re.search(rf"(\d+|(\d+\.\d+)){character}", message._text)
            if match:
                if character == "m":
                    mute_seconds += int(
                        float(match.string[match.start() : match.end() - 1])
                        * 60
                        // 1
                    )
                if character == "h":
                    mute_seconds += int(
                        float(match.string[match.start() : match.end() - 1])
                        * 3600
                        // 1
                    )
                if character == "d":
                    mute_seconds += int(
                        float(match.string[match.start() : match.end() - 1])
                        * 86400
                        // 1
                    )
                if character == "w":
                    mute_seconds += int(
                        float(match.string[match.start() : match.end() - 1])
                        * 604800
                        // 1
                    )
        try:
            if mute_seconds > 30:
                await client.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    ChatPermissions(),
                    datetime.now() + timedelta(seconds=mute_seconds),
                )
                from_user = message.reply_to_message.from_user
                mute_time: Dict[str, int] = {
                    "days": mute_seconds // 86400,
                    "hours": mute_seconds % 86400 // 3600,
                    "minutes": mute_seconds % 86400 % 3600 // 60,
                }
                message_text = (
                    f"{from_user.first_name} was muted for"
                    f" {((str(mute_time['days']) + ' day') if mute_time['days'] > 0 else '') + ('s' if mute_time['days'] > 1 else '')}"
                    f" {((str(mute_time['hours']) + ' hour') if mute_time['hours'] > 0 else '') + ('s' if mute_time['hours'] > 1 else '')}"
                    f" {((str(mute_time['minutes']) + ' minute') if mute_time['minutes'] > 0 else '') + ('s' if mute_time['minutes'] > 1 else '')}"
                    + f"\n{'Reason: ' + cause.split(' ', maxsplit=2)[2] + '' if len(cause.split()) > 2 else ''}"
                )
                while "  " in message_text:
                    message_text = message_text.replace("  ", " ")
            else:
                await client.restrict_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    ChatPermissions(),
                )
                message_text = (
                    f"{message.reply_to_message.from_user.first_name} was muted indefinitely!"
                    + f"\n{'Reason: ' + cause.split(' ', maxsplit=1)[1] + '' if len(cause.split()) > 1 else ''}"
                )
            await message.edit(message_text)
        except UserAdminInvalid:
            await message.edit("No rights!")
        except ChatAdminRequired:
            await message.edit("No rights!")
        except Exception as e:
            await message.edit(format_exc(e))
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                user_to_unmute = await client.get_users(cause.split(" ")[1])
                mute_seconds: int = 0
                for character in "mhdw":
                    match = re.search(
                        rf"(\d+|(\d+\.\d+)){character}", message._text
                    )
                    if match:
                        if character == "m":
                            mute_seconds += int(
                                float(
                                    match.string[
                                        match.start() : match.end() - 1
                                    ]
                                )
                                * 60
                                // 1
                            )
                        if character == "h":
                            mute_seconds += int(
                                float(
                                    match.string[
                                        match.start() : match.end() - 1
                                    ]
                                )
                                * 3600
                                // 1
                            )
                        if character == "d":
                            mute_seconds += int(
                                float(
                                    match.string[
                                        match.start() : match.end() - 1
                                    ]
                                )
                                * 86400
                                // 1
                            )
                        if character == "w":
                            mute_seconds += int(
                                float(
                                    match.string[
                                        match.start() : match.end() - 1
                                    ]
                                )
                                * 604800
                                // 1
                            )
                try:
                    if mute_seconds > 30:
                        await client.restrict_chat_member(
                            message.chat.id,
                            user_to_unmute.id,
                            ChatPermissions(),
                            datetime.now() + timedelta(seconds=mute_seconds),
                        )
                        mute_time: Dict[str, int] = {
                            "days": mute_seconds // 86400,
                            "hours": mute_seconds % 86400 // 3600,
                            "minutes": mute_seconds % 86400 % 3600 // 60,
                        }
                        message_text = (
                            f"{user_to_unmute.first_name} was muted for"
                            f" {((str(mute_time['days']) + ' day') if mute_time['days'] > 0 else '') + ('s' if mute_time['days'] > 1 else '')}"
                            f" {((str(mute_time['hours']) + ' hour') if mute_time['hours'] > 0 else '') + ('s' if mute_time['hours'] > 1 else '')}"
                            f" {((str(mute_time['minutes']) + ' minute') if mute_time['minutes'] > 0 else '') + ('s' if mute_time['minutes'] > 1 else '')}"
                            + f"\n{'Reason: ' + cause.split(' ', maxsplit=3)[3] + '' if len(cause.split()) > 3 else ''}"
                        )
                        while "  " in message_text:
                            message_text = message_text.replace("  ", " ")
                    else:
                        await client.restrict_chat_member(
                            message.chat.id,
                            user_to_unmute.id,
                            ChatPermissions(),
                        )
                        message_text = (
                            f"{user_to_unmute.first_name} was muted indefinitely"
                            + f"\n{'Reason: ' + cause.split(' ', maxsplit=2)[2] + '' if len(cause.split()) > 2 else ''}"
                        )
                    await message.edit(message_text)
                except UserAdminInvalid:
                    await message.edit("No rights!")
                except ChatAdminRequired:
                    await message.edit("No rights!")
                except Exception as e:
                    await message.edit(format_exc(e))
            except PeerIdInvalid:
                await message.edit("User is not found!")
            except UsernameInvalid:
                await message.edit("User is not found!")
            except IndexError:
                await message.edit("User is not found!")
        else:
            await message.edit("user_id or username!")
    else:
        await message.edit("Unsupported!")


@Client.on_message(filters.command("demote", prefix) & filters.me)
async def _demote(client: Client, message: Message):
    cause = _text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if message.reply_to_message.from_user:
            try:
                await client.promote_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    privileges=ChatPrivileges(
                        is_anonymous=False,
                        can_manage_chat=False,
                        can_change_info=False,
                        can_post_messages=False,
                        can_edit_messages=False,
                        can_delete_messages=False,
                        can_manage_video_chats=False,
                        can_restrict_members=False,
                        can_invite_users=False,
                        can_pin_messages=False,
                        can_promote_members=False,
                    ),
                )
                await message.edit(
                    f"{message.reply_to_message.from_user.first_name} demoted!"
                    + f"\n{'Reason: ' + cause.split(' ', maxsplit=1)[1] + '' if len(cause.split()) > 1 else ''}"
                )
            except UserAdminInvalid:
                await message.edit("No rights!")
            except ChatAdminRequired:
                await message.edit("No rights!")
            except Exception as e:
                await message.edit(format_exc(e))
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                promote_user = await client.get_users(cause.split(" ")[1])
                try:
                    await client.promote_chat_member(
                        message.chat.id,
                        promote_user.id,
                        privileges=ChatPrivileges(
                            is_anonymous=False,
                            can_manage_chat=False,
                            can_change_info=False,
                            can_post_messages=False,
                            can_edit_messages=False,
                            can_delete_messages=False,
                            can_manage_video_chats=False,
                            can_restrict_members=False,
                            can_invite_users=False,
                            can_pin_messages=False,
                            can_promote_members=False,
                        ),
                    )
                    await message.edit(
                        f"{promote_user.first_name} demoted!"
                        + f"\n{'Reason: ' + cause.split(' ', maxsplit=2)[2] + '' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("No rights!")
                except ChatAdminRequired:
                    await message.edit("No rights!")
                except Exception as e:
                    await message.edit(format_exc(e))
            except PeerIdInvalid:
                await message.edit("User is not found!")
            except UsernameInvalid:
                await message.edit("User is not found!")
            except IndexError:
                await message.edit("User is not found!")
        else:
            await message.edit("user_id or username!")
    else:
        await message.edit("Unsupported!")


@Client.on_message(filters.command(["promote"], prefix) & filters.me)
async def _promote(client: Client, message: Message):
    cause = _text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if message.reply_to_message.from_user:
            try:
                await client.promote_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    privileges=ChatPrivileges(
                        can_delete_messages=True,
                        can_restrict_members=True,
                        can_invite_users=True,
                        can_pin_messages=True,
                    ),
                )
                if len(cause.split()) > 1:
                    await client.set_administrator_title(
                        message.chat.id,
                        message.reply_to_message.from_user.id,
                        cause.split(maxsplit=1)[1],
                    )
                await message.edit(
                    f"{message.reply_to_message.from_user.first_name} promoted!"
                    + f"\n{'Tittle: ' + cause.split(' ', maxsplit=1)[1] + '' if len(cause.split()) > 1 else ''}"
                )
            except UserAdminInvalid:
                await message.edit("No rights!")
            except ChatAdminRequired:
                await message.edit("No rights!")
            except Exception as e:
                await message.edit(format_exc(e))
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                promote_user = await client.get_users(cause.split(" ")[1])
                try:
                    await client.promote_chat_member(
                        message.chat.id,
                        promote_user.id,
                        privileges=ChatPrivileges(
                            can_delete_messages=True,
                            can_restrict_members=True,
                            can_invite_users=True,
                            can_pin_messages=True,
                        ),
                    )
                    if len(cause.split()) > 1:
                        await client.set_administrator_title(
                            message.chat.id,
                            promote_user.id,
                            f"\n{cause.split(' ', maxsplit=2)[2] if len(cause.split()) > 2 else None}",
                        )
                    await message.edit(
                        f"{promote_user.first_name} promoted!"
                        + f"\n{'Tittle: ' + cause.split(' ', maxsplit=2)[2] + '' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("No rights!")
                except ChatAdminRequired:
                    await message.edit("No rights!")
                except Exception as e:
                    await message.edit(format_exc(e))
            except PeerIdInvalid:
                await message.edit("User is not found!")
            except UsernameInvalid:
                await message.edit("User is not found!")
            except IndexError:
                await message.edit("User is not found!")
        else:
            await message.edit("user_id or username!")
    else:
        await message.edit("Unsupported!")


@Client.on_message(filters.command("antich", prefix))
async def _antich(client: Client, message: Message):
    if len(message.command) == 1:
        if db.get("core.ats", f"antich{message.chat.id}", False):
            await message.edit(
                "Blocking channels in this chat is enabled.\n"
                f"Deactivated: <code>{prefix}antich off</code>"
            )
        else:
            await message.edit(
                "Blocking channels in this chat is disabled.\n"
                f"Enable with: <code>{prefix}antich on</code>"
            )
    elif message.command[1] == "on":
        db.set("core.ats", f"antich{message.chat.id}", True)
        group = await client.get_chat(message.chat.id)
        if group.linked_chat:
            db.set("core.ats", f"linked{message.chat.id}", group.linked_chat.id)
        else:
            db.set("core.ats", f"linked{message.chat.id}", 0)
        await message.edit("Blocking channels in this chat enabled.")
    elif message.command[1] == "off":
        db.set("core.ats", f"antich{message.chat.id}", False)
        await message.edit("Blocking channels in this chat disabled.")
    else:
        await message.edit(f"Usage: <code>{prefix}antich </code>[on|off]")

    _cache()


@Client.on_message(filters.command("dh", prefix))
async def _dh(client: Client, message: Message):
    cause = _text(message)
    if message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if message.reply_to_message.from_user:
            try:
                user_for_delete, name = await _user(message)
                channel = await client.resolve_peer(message.chat.id)
                user_id = await client.resolve_peer(user_for_delete)
                await client.invoke(
                    functions.channels.DeleteParticipantHistory(
                        channel=channel, participant=user_id
                    )
                )

                await message.edit(
                    f"History from {name} was deleted!"
                    + f"\n{'Reason: ' + cause.split(maxsplit=1)[1] + '' if len(cause.split()) > 1 else ''}"
                )
            except UserAdminInvalid:
                await message.edit("No rights!")
            except ChatAdminRequired:
                await message.edit("No rights!")
            except Exception as e:
                await message.edit(format_exc(e))
        else:
            await message.edit("Reply on user message!")
    elif not message.reply_to_message and message.chat.type not in [
        "private",
        "channel",
    ]:
        if len(cause.split()) > 1:
            try:
                if await _check(cause.split(" ")[1]) == "channel":
                    user_to_delete = await client.get_chat(cause.split(" ")[1])
                elif await _check(cause.split(" ")[1]) == "user":
                    user_to_delete = await client.get_users(cause.split(" ")[1])
                else:
                    await message.edit("Invalid user type!")
                    return

                name = (
                    user_to_delete.first_name
                    if getattr(user_to_delete, "first_name", None)
                    else user_to_delete.title
                )

                try:
                    channel = await client.resolve_peer(message.chat.id)
                    user_id = await client.resolve_peer(user_to_delete.id)
                    await client.invoke(
                        functions.channels.DeleteParticipantHistory(
                            channel=channel, participant=user_id
                        )
                    )
                    await message.edit(
                        f"History from {name} was deleted!"
                        + f"\n{'Reason: ' + cause.split(' ', maxsplit=2)[2] + '' if len(cause.split()) > 2 else ''}"
                    )
                except UserAdminInvalid:
                    await message.edit("No rights!")
                except ChatAdminRequired:
                    await message.edit("No rights!")
                except Exception as e:
                    await message.edit(format_exc(e))
            except PeerIdInvalid:
                await message.edit("User is not found!")
            except UsernameInvalid:
                await message.edit("User is not found!")
            except IndexError:
                await message.edit("User is not found!")
        else:
            await message.edit("user_id or username!")
    else:
        await message.edit("Unsupported!")


@Client.on_message(filters.command("rs", prefix))
@_reply
async def _rs(client: Client, message: Message):
    try:
        channel = await client.resolve_peer(message.chat.id)

        user_id, name = await _user(message)
        peer = await client.resolve_peer(user_id)
        await client.invoke(
            functions.channels.ReportSpam(
                channel=channel,
                participant=peer,
                id=[message.reply_to_message.id],
            )
        )
    except Exception as e:
        await message.edit(format_exc(e))
    else:
        await message.edit(f"Message from {name} was reported!")


@Client.on_message(filters.command("pin", prefix) & filters.me)
@_reply
async def _pin(_, message: Message):
    try:
        await message.reply_to_message.pin()
        await message.edit("Pinned!")
    except Exception as e:
        await message.edit(format_exc(e))


@Client.on_message(filters.command("unpin", prefix) & filters.me)
@_reply
async def _unpin(_, message: Message):
    try:
        await message.reply_to_message.unpin()
        await message.edit("Unpinned!")
    except Exception as e:
        await message.edit(format_exc(e))


@Client.on_message(filters.command("ro", prefix) & filters.me)
async def _ro(client: Client, message: Message):
    try:
        perms = message.chat.permissions
        perms_list = [
            perms.can_send_messages,
            perms.can_send_media_messages,
            perms.can_send_other_messages,
            perms.can_send_polls,
            perms.can_add_web_page_previews,
            perms.can_change_info,
            perms.can_invite_users,
            perms.can_pin_messages,
        ]
        db.set("core.ats", f"ro{message.chat.id}", perms_list)

        try:
            await client.set_chat_permissions(
                message.chat.id, ChatPermissions()
            )
        except (UserAdminInvalid, ChatAdminRequired):
            await message.edit("No rights!")
        else:
            await message.edit(
                "Read-only mode activated!\n"
                f"Deactivated: <code>{prefix}unro</code>"
            )
    except Exception as e:
        await message.edit(format_exc(e))


@Client.on_message(filters.command("unro", prefix) & filters.me)
async def _unro(client: Client, message: Message):
    try:
        perms_list = db.get(
            "core.ats",
            f"ro{message.chat.id}",
            [True, True, True, False, False, False, False, False],
        )
        perms = ChatPermissions(
            can_send_messages=perms_list[0],
            can_send_media_messages=perms_list[1],
            can_send_other_messages=perms_list[2],
            can_send_polls=perms_list[3],
            can_add_web_page_previews=perms_list[4],
            can_change_info=perms_list[5],
            can_invite_users=perms_list[6],
            can_pin_messages=perms_list[7],
        )

        try:
            await client.set_chat_permissions(message.chat.id, perms)
        except (UserAdminInvalid, ChatAdminRequired):
            await message.edit("No rights!")
        else:
            await message.edit("Read-only mode disabled!")
    except Exception as e:
        await message.edit(format_exc(e))

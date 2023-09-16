# Copyright (C) 2020 - Dragon Userbot

import os
import re

from meval import meval
from io import StringIO
from contextlib import redirect_stdout

from subprocess import Popen, PIPE, TimeoutExpired
from pyrogram import Client, filters
from pyrogram.types import Message

from utils.format import format_exc
from utils.database import prefix


danger = [
    "env", 
    "config.env"
    "MONGODB_URL"
    "SESSION_STRING",
    "export_session_sting"
    ] 

@Client.on_message(filters.command("sh", prefix) & filters.me)
async def _shell(_, message: Message):
    if len(message.command) < 2:
        return await message.edit(
            "Specify the command in message text!")

    cmd_text = message.text.split(maxsplit=1)[1]
    cmd_obj = Popen(
        cmd_text,
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
        text=True,
    )

    char = "#" if os.getuid() == 0 else "$"
    text = f"{char} <code>{cmd_text}</code>\n\n"
    if any(re.search(
        rf'\b\w*{re.escape(keyword)}\w*\b',
        text,
    ) for keyword in danger):
        return await message.reply(
            "WARNING!\n\n" \
            "This command contains potentially dangerous content!",
            reply_to_message_id=message.id
        )
    

    await message.edit(f"{text}Running...")
    try:
        stdout, stderr = cmd_obj.communicate(timeout=60)
    except TimeoutExpired:
        text += "Timeout expired! (60s)"
    else:
        if stdout:
            if len(stdout) > 4096:
                with open(
                    "output.txt",
                    "w",
                    encoding="utf-8"
                ) as output_file:
                    output_file.write(stdout)
                text += "Output:\n<code>" \
                        "Was too long, sent as a file..." \
                        "</code>"
                await message.reply_document(
                    "output.txt")
                os.remove("output.txt")
            else:
                text += "Output:\n" \
                        f"<code>{stdout}</code>"
        if stderr:
            text += f"\n<code>{stderr}</code>"
    await message.edit(text)
    cmd_obj.kill()


@Client.on_message(filters.command("ex", prefix) & filters.me)
async def _exec(client: Client, message: Message):
    if len(message.command) == 1:
        return await message.edit(
            "Code to execute isn't provided!")

    reply = message.reply_to_message

    code = message.text.split(maxsplit=1)[1]
    if any(re.search(
        rf'\b\w*{re.escape(keyword)}\w*\b',
        code,
    ) for keyword in danger):
        return await message.reply(
            "WARNING!\n\n" \
            "This command contains potentially dangerous content!",
            reply_to_message_id=message.id
        )
    stdout = StringIO()

    await message.edit("Executing...")

    try:
        with redirect_stdout(stdout):
            exec(code)
        output = stdout.getvalue()
        result = "<pre language=python>" \
                 f"{code}</pre>" \
                 "\n\nOutput:\n" \
                 f"<code>{output}</code>"
        if len(result) > 4096:
            with open(
                "output.txt",
                "w",
                encoding="utf-8"
            ) as output_file:
                output_file.write(stdout)
            await message.edit(
                f"<pre language=python>{code}" \
                "</pre>\n\n" \
                "Output:\n<code>" \
                "Was too long, sent as a file..." \
                "</code>"
            )
            await message.reply_document("output.txt")

            os.remove("output.txt")
        else:
            await message.edit(result)

    except Exception as e:
        await message.edit(
            f"<code>{code}</code>"
            "\n\n" \
            "Error:\n" \
            f"{format_exc(e)}"
        )


@Client.on_message(filters.command("ev", prefix) & filters.me)
async def _eval_(client: Client, message: Message):
    if len(message.command) == 1:
        return await message.edit(
            "Code to evaluate isn't provided!")
    
    code = message.text.split(maxsplit=1)[1]
    if any(re.search(
        rf'\b\w*{re.escape(keyword)}\w*\b',
        code,
    ) for keyword in danger):
        return await message.reply(
            "WARNING!\n\n" \
            "This command contains potentially dangerous content!",
            reply_to_message_id=message.id
        )

    evars = {
        "c": client,
        "m": message,
        "r": message.reply_to_message,
        "chat": message.chat,
        "user": (message.reply_to_message or message).from_user,
        "client": client,
        "message": message,
    }

    try:
        output = await meval(code, globals(), **evars)
        output = str(output)
        result = f"<pre language=python>{code}</pre>" \
                 "\n\nOutput:\n" \
                 f"<code>{output}</code>" 
        if len(result) > 4096:
            with open(
                "output.txt",
                "w",
                encoding="utf-8",
            ) as output_file:
                output_file.write(output)
            await message.edit(
                f"<pre language=python>{code}</pre>\n\n" \
                "Output:\n" \
                "<code>Was too long, sent as a file...</code>",
            )
            await message.reply_document(
                "output.txt")
                
            os.remove("output.txt")
        else:
            await message.edit(result)
    
    except Exception as e:
        await message.edit(
            f"<code>{code}</code>" \
            "\n\n" \
            "Error:\n" \
            f"<code>{format_exc(e)}</code>")
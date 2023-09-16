# Copyright (C) 2020 - Dragon Userbot

import traceback

from pyrogram import errors

from .database import prefix
from .help import modules


def format_exc(e: Exception, suffix="") -> str:
    traceback.print_exc()
    if isinstance(e, errors.RPCError):
        return (
            f"<code>[{e.CODE} {e.ID or e.NAME}] — {e.MESSAGE.format(value=e.value)}</code>\n\n{suffix}"
        )
    return (
        f"<code>{e.__class__.__name__}: {e}</code>\n\n{suffix}"
    )


def format_help(module_name: str):
    commands = modules[module_name]

    help_text = f"Help for [{module_name}]\n\n"

    for command, desc in commands.items():
        cmd = command.split(maxsplit=1)
        args = " " + cmd[1] if len(cmd) > 1 else ""
        help_text += f"<code>{prefix}{cmd[0]}</code>{args}: {desc}.\n"

    return help_text
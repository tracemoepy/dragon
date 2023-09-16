# Copyright (C) 2020 - Dragon Userbot

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.format import format_help
from utils.help import modules
from utils.helpers.updater import restart
from utils.database import db, prefix


@Client.on_message(filters.command("help", prefix) & filters.me)
async def _help(_, message: Message):
    if len(message.command) == 1:
        msg_edited = False
        text = (
            "For more help on how to use a command,"
            "\ntype: "
            f"<code>{prefix}help </code>"
            "<code>[module/command]</code>"
            "\n\n"
            "Available Modules\n"
        )
        
        sorted_modules = sorted(modules.items(), key=lambda x: x[0].title())
        for module_name, module_commands in sorted_modules:
            text += "   {}: {}\n".format(
                module_name.title(),
                " ".join(
                    [
                        f"<code>{prefix + cmd_name.split()[0]}</code>"
                        for cmd_name in module_commands.keys()
                    ]
                ),
            )
            if len(text) >= 2048:
                text += ""
                if msg_edited:
                    await message.reply(text, disable_web_page_preview=True)
                else:
                    await message.edit(text, disable_web_page_preview=True)
                    msg_edited = True
                text = ""

        text += "\nTotal: " \
                f"{len(modules)} Modules"

        if msg_edited:
            await message.reply(text, disable_web_page_preview=True)
        else:
            await message.edit(text, disable_web_page_preview=True)
    elif message.command[1].lower() in modules:
        await message.edit(format_help(message.command[1].lower()))
    else:
        command_name = message.command[1].lower()
        for name, commands in modules.items():
            for command in commands.keys():
                if command.split()[0] == command_name:
                    cmd = command.split(maxsplit=1)
                    cmd_desc = commands[command]
                    return await message.edit(f"""
Module [<code>{prefix}help {name}</code>]

<code>{prefix}{cmd[0]}</code> {cmd_desc}.
                    """)
        await message.edit(
            f"Module {command_name} not found."
        )


@Client.on_message(filters.command("prefix", prefix) & filters.me)
async def _prefix(_, message: Message):
    if len(message.command) > 1:
        pref = message.command[1]
        db.set("core.main", "prefix", pref)
        await message.edit(
            f"Prefix [<code>{pref}</code>] is set!"
        )
        restart()
    else:
        await message.edit(
            "The prefix must not be empty!"
        )
    await message
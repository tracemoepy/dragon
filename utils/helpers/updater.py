import os
import sys
import subprocess

from pyrogram import __version__


python = f"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"
pyrogram = f"{__version__}"


DESC = f"""
<b>Dragon-Fork</b> is a Telegram userbot based on <a href=https://github.com/Dragon-Userbot/Dragon-Userbot><b>Dragon-Userbot</b></a> (in case you didn't know, selfbot/userbot are used to automate user accounts). So how does it work? It works in a very simple way, using the pyrogram library, a python script connects to your account (creating a new session) and catches your commands.

Using selfbot/userbot is against Telegram's Terms of Service, and you may get banned for using it if you're not careful.

Running on <b>Python v{python}</b> with <b>Pyrogram v{pyrogram}</b>
"""


def restart() -> None:
    os.execvp(
            sys.executable,
            [
                sys.executable,
                "main.py"
            ]
        )


def uppip() -> None:
    subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-U",
                "pip"
            ]
        )


def gpull() -> None:
    subprocess.run(
            [
                "git",
                "pull",
                "--rebase",
                "-f"
            ]
        )


def upreq() -> None:
    subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-U",
                "-r",
                "requirements.txt",
            ]
        )
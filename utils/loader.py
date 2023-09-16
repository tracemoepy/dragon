# Copyright (C) 2020 - Dragon Userbot

import re
import sys
import importlib

from typing import Dict
from types import ModuleType

from pyrogram import Client, types

from .help import modules


requirements_list = []

META_COMMENTS = re.compile(r"^ *# *meta +(\S+) *: *(.*?)\s*$", re.MULTILINE)


def parse_meta(code: str) -> Dict[str, str]:
    try:
        groups = META_COMMENTS.search(code).groups()
    except AttributeError:
        return {}

    return {groups[i]: groups[i + 1] for i in range(0, len(groups), 2)}
    
    
async def _loader(
    module_name: str,
    client: Client,
    message: types.Message = None,
    core=False,
) -> ModuleType:
    path = f"modules.{'custom_modules.' if not core else ''}{module_name}"

    with open(f"{path.replace('.', '/')}.py", encoding="utf-8") as f:
        code = f.read()
        
    meta = parse_meta(code)
    packages = meta.get("requires", "").split()
    requirements_list.extend(packages)

    try:
        module = importlib.import_module(path)
    except ImportError as e:
        if core:
            raise

        if not packages:
            raise

        if message:
            await message.edit(
                f"Installing requirements: {' '.join(packages)}"
            )

        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m",
            "pip",
            "install",
            "-U",
            *packages,
        )
        try:
            await asyncio.wait_for(proc.wait(), timeout=300)
        except asyncio.TimeoutError:
            if message:
                await message.edit(
                    "Timeout while installed requirements. Try to install them manually"
                )
            raise TimeoutError("timeout while installing requirements") from e

        if proc.returncode != 0:
            if message:
                await message.edit(
                    f"Failed to install requirements (pip exited with code {proc.returncode}). "
                    f"Check logs for futher info"
                )
            raise RuntimeError("failed to install requirements") from e

        module = importlib.import_module(path)

    for name, obj in vars(module).items():
        for handler, group in getattr(obj, "handlers", []):
            client.add_handler(handler, group)

    module.__meta__ = meta

    return module
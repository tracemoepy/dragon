from utils.help import modules


modules["access"] = {
    "help": "[module/command] Get common module help",
    "prefix": "[x] Change prefix",
}

modules["admins"] = {
    "ban": "[reply|user] [reason] [rs] [dh] Ban user in chat",
    "unban": "[reply|user] [reason] Unban user in chat",
    "kick": "[reply|user] [reason] [rs] [dh] Kick user out of chat",
    "mute": "[reply|user] [m|h|d|w] [reason] Mute user in chat",
    "unmute": "[reply|user] [reason] Unmute user in chat",
    "promote": "[reply|user] [tittle] Promote user in chat",
    "demote": "[reply|user] [reason] Demote user in chat",
    "pin": "[reply] Pin replied message",
    "unpin": "[reply] Unpin replied message",
    "ro": "Enable read-only mode",
    "unro": "Disable read-only mode",
    "antich": "[on|off] Turn on/off blocking channels in this chat",
    "zombie": "Kick all deleted accounts",
    "dh": "[reply|user] [reason] Delete history from member in chat",
    "rs": "[reply] Report spam message in chat",
}

modules["debug"] = {
    "sh": "[command] Excute command in shell",
    "ev": "[code] Evaluate code",
    "ex": "[python code] Excute python code",
}

modules["message"] = {
    "del": "[reply] Delete message by replied",
    "purge": "[reply] Prune messages, start from replied",
    "purgeme": "[int] Prune your message by amount",
}

modules["noted"] = {
    "notes": "Get list available notes",
    "get": "[name] Get saved note",
    "save": "[reply] [name] Save note",
    "clear": "[name] Delete note",
}

modules["security"] = {
    "antipm": "[on|off] When enabled, deletes all messages from users who are not in the contact",
    "pmreport": "[on|off] Enable spam reporting",
    "pmblock": "[on|off] Enable user blocking",
}

modules["system"] = {
    "about": "Description of userbot",
    "ping": "Round trip time",
    "restart": "Restart userbot",
    "update": "Update userbot",
}

modules["voicechat"] = {
    "vc": "[on|off] Toggle to start/stop voice chat",
    "join": "Join to voice chat",
    "leave": "Leave from voice chat",
}

modules["Utils"] = {
    "afk": "[reason] Away from keyboard",
    "copy": "[link] Copy telegram message by its message link",
    "wow": "[w/o prefix] Save media to saved message (also work media with timer)",
    "profile": "[reply|user] Get profile info of user",
}
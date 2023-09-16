# Copyright (C) 2020 - Dragon Userbot

class ModulesHelpDict(dict):
    def append(self, obj: dict):
        # convert help from old to new type
        module_name = list(obj.keys())[0]
        cmds = obj[module_name]
        commands = {}
        for cmd in cmds:
            cmd_name = list(cmd.keys())[0]
            cmd_desc = cmd[cmd_name]
            commands[cmd_name] = cmd_desc
        self[module_name] = commands

modules = ModulesHelpDict()

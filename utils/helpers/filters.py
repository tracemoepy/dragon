from pyrogram import filters

from utils.database import db, afk_info


pmstatus = filters.create(
    lambda _, __, ___: db.get("core.antipm", "status", False)
)

contacts = filters.create(
    lambda _, __, message: message.from_user.is_contact
)

supports = filters.create(
    lambda _, __, message: message.chat.is_support
)

onafk = filters.create(
    lambda _, __, ___: afk_info["is_afk"]
)

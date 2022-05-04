from pyrogram import Client, filters
from database import botusers


@Client.on_message(filters.command("start") & filters.private)
async def start(c, m):

    await botusers.new(m.from_user)
    await m.reply("Hello")

from pyrogram import Client, filters


@Client.on_message(filters.command("start") & filters.private)
async def start(c, m):

    await m.reply("Hello")

from pyrogram import Client, filters

from pyromod.helpers import ikb


@Client.on_message(filters.regex("/help"))
async def help(c, m):

    await m.reply(
        text=f"""
Hello {m.from_user.first_name} 👋. I am the bot 🤖 that is going to take over the world 🌍 soon, real soon...

I am the **{(await c.get_me()).first_name}**, the ultimate Meme madness. I can generate 🆒 memes 4 u ╰(*°▽°*)╯
""",
        parse_mode="md",
        reply_markup=ikb(
            [
                [
                    ("Imgflip Meme Generator", "imgflipHelp"),
                ],
                [
                    ("F in Chat", "FHelp"),
                ],
            ]
        ),
    )

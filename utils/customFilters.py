from pyrogram import filters
from utils import imgflip


async def is_recent_imgflip_meme(_, __, m):
    data = m.query.split(" ")[0].lower()

    if data in imgflip.recent_memes_by_name:
        return True

    else:
        return False


isRecentImgflipMeme = filters.create(is_recent_imgflip_meme)


async def imgflip_format_true(_, __, m):

    name = m.query.split(" ")[0].lower().strip()

    if m.query.strip() != name:

        memeInfo = imgflip.recent_memes_by_name[name]
        text = (m.query.split(" ", 1)[1].strip()).split(";")

        if len(text) == memeInfo["box_count"]:
            return True

        else:
            return False

    else:
        return False


imgflipFormatTrue = filters.create(imgflip_format_true)


async def inline_prediction(_, __, m):

    data = m.query.split(" ")[0].lower().strip()

    if data != ("f" or "tweet"):

        for meme in imgflip.recent_memes_by_name:
            if data in meme:
                return True

        return False


inlinePrediction = filters.create(inline_prediction)


async def f_in_chat(_, __, m):

    data = m.query.split(" ")[0].lower().strip()

    return data == "f"


fInChat = filters.create(f_in_chat)

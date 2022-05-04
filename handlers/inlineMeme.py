from pyrogram import Client, filters
from pyrogram.types import (
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto,
)
from utils import imgflip, customFilters


@Client.on_inline_query(customFilters.isRecentImgflipMeme)
async def callback(c, m):

    name = m.query.split(" ")[0].lower()

    # if there is only the memename in the callback, we answer with the meme info

    if len(m.query.split(" ")) == 1 and m.query.lower().strip() == name:

        memeInfo = imgflip.recent_memes_by_name[name]

        await m.answer(
            results=[
                InlineQueryResultArticle(
                    title=f"Template: {' '.join(name.split('_')).title()}",
                    description=f"This template requires {memeInfo['box_count']} caption(s) separated by ;",
                    thumb_url=memeInfo["url"],
                    input_message_content=InputTextMessageContent(
                        message_text=f"**❌ You forgot to give me the {memeInfo['box_count']} caption(s) required for this template.**[­]({memeInfo['url']})",
                        parse_mode="md",
                        disable_web_page_preview=False,
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Try again 🔁",
                                    switch_inline_query_current_chat=m.query.strip(),
                                )
                            ]
                        ],
                    ),
                )
            ],
            switch_pm_text="View all templates",
            switch_pm_parameter="imgflip_templates",
            cache_time=1,
        )

    # if there is a text in the callback, we create the meme
    else:

        memeInfo = imgflip.recent_memes_by_name[name]
        text = (m.query.split(" ", 1)[1].strip()).split(";")

        if len(text) == memeInfo["box_count"]:

            await m.answer(
                results=[
                    InlineQueryResultPhoto(
                        title=f"Template: {' '.join(name.split('_')).title()}",
                        photo_url=memeInfo["url"],
                        thumb_url=memeInfo["url"],
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "Creating meme... ⚙️",
                                        url=f"https://t.me/su_Bots",
                                    )
                                ]
                            ],
                        ),
                    ),
                ],
                switch_pm_text="Click the photo below to send",
                switch_pm_parameter=f"redirect_created",
                cache_time=1,
            )

        else:
            await m.answer(
                results=[
                    InlineQueryResultArticle(
                        title=f"Template: {' '.join(name.split('_')).title()}",
                        description=f"Given captions: {len(text)}\nRequired captions: {memeInfo['box_count']}",
                        thumb_url=memeInfo["url"],
                        input_message_content=InputTextMessageContent(
                            message_text=f"**❌ You gave me {len(text)} caption(s) instead of the required {memeInfo['box_count']} for this template.**[­]({memeInfo['url']})",
                            parse_mode="md",
                            disable_web_page_preview=False,
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "Try again 🔁",
                                        switch_inline_query_current_chat=m.query.strip(),
                                    )
                                ]
                            ],
                        ),
                    )
                ],
                cache_time=1,
            )


@Client.on_chosen_inline_result(
    customFilters.isRecentImgflipMeme & customFilters.imgflipFormatTrue
)
async def chosen_imgflip_meme(c, m):

    name = m.query.split(" ")[0].lower().strip()
    memeInfo = imgflip.recent_memes_by_name[name]
    text = (m.query.split(" ", 1)[1].strip()).split(";")

    memeURL = await imgflip.createMeme(memeInfo, text)

    await c.edit_inline_media(
        inline_message_id=m.inline_message_id,
        media=InputMediaPhoto(memeURL["data"]["url"]),
    )

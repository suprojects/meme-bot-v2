from pyrogram import Client, filters
from pyrogram.types import (
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from pyrogram.errors import exceptions
from utils import imgflip, customFilters


@Client.on_inline_query(customFilters.inlinePrediction)
async def inlineAutocomplete(c, m):

    name = m.query.split(" ")[0].lower().strip()
    suggestions = []

    if name:
        for meme in imgflip.recent_memes_by_name:
            if name in meme:
                suggestions.append(imgflip.recent_memes_by_name[meme])

    results = []

    for suggestion in suggestions:

        results.append(
            InlineQueryResultArticle(
                title=f"Template: {' '.join(suggestion['name'].split('_')).title()}",
                description=f"Command: {suggestion['name']}\nModule: Imgflip",
                thumb_url=suggestion["url"],
                input_message_content=InputTextMessageContent(
                    message_text=f"**Template: {' '.join(suggestion['name'].split('_')).title()}\nCommand: {suggestion['name']}\nCaptions required: {suggestion['box_count']}**[­]({suggestion['url']})",
                    parse_mode="md",
                    disable_web_page_preview=False,
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Use this template in this chat",
                                switch_inline_query_current_chat=suggestion["name"],
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Use this template in another chat",
                                switch_inline_query=suggestion["name"],
                            ),
                        ],
                    ],
                ),
            )
        )

    await m.answer(
        results=results if len(results) <= 50 else results[0:50],
        cache_time=1,
        switch_pm_text="More than 50 templates, type more to filter"
        if len(results) >= 50
        else None,
        switch_pm_parameter="imgflip_templates" if len(results) >= 50 else None,
    )


@Client.on_inline_query(~customFilters.inlinePrediction)
async def unknownInline(c, m):
    await m.answer(
        results=[
            InlineQueryResultArticle(
                title="Unknown command",
                description="Try /help in PM",
                input_message_content=InputTextMessageContent(
                    message_text=f"**❌ Unrecognised command**",
                    parse_mode="md",
                    disable_web_page_preview=False,
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "View help",
                                url=f"https://t.me/{(await c.get_me()).username}?start=help",
                            )
                        ]
                    ],
                ),
            )
        ]
    )

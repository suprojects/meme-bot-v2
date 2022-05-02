from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from utils import customFilters


@Client.on_inline_query(customFilters.fInChat)
async def inlineFInChat(c, m):

    param = " ".join(m.query.split(" ")[1:])

    await m.answer(
        results=[
            InlineQueryResultArticle(
                title="Press F",
                thumb_url="https://telegra.ph/file/7086f123ecd4af6a8f343.jpg",
                description=f"for {param}" if param else "to pay respects",
                input_message_content=InputTextMessageContent(
                    message_text=f"**Press F** for {param}"
                    if param
                    else "**Press F** to pay respects",
                    parse_mode="md",
                    disable_web_page_preview=True,
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="F",
                                callback_data="f_0",
                            )
                        ]
                    ],
                ),
            )
        ],
        switch_pm_text="Module help",
        switch_pm_parameter=f"help_f",
        cache_time=1,
    )


@Client.on_callback_query(filters.regex("^f_\d+$"))
async def f_button(c, m):

    count = int(m.data.split("_")[1]) + 1

    await c.edit_inline_reply_markup(
        inline_message_id=m.inline_message_id,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=f"{count} F's" if count != 1 else "1 F in Chat",
                        callback_data=f"f_{count}",
                    )
                ]
            ]
        ),
    )

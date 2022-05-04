from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto
from pyrogram.errors.exceptions import bad_request_400

from pyromod.nav import Pagination
from pyromod.helpers import ikb

import random

from utils import imgflip


@Client.on_message(filters.regex("/imgflip"))
async def imgflipHelp(c, m):

    await m.reply_photo(
        caption="Available Imgflip Meme Templates",
        photo="https://telegra.ph/file/9c7c7559dc455a700f25f.png",
        reply_markup=ikb(returnKeyboard(index=1)),
    )


@Client.on_callback_query(filters.regex("imgflipHelp$"))
async def ImgflipMainMenu(c, m):

    randomTemplate = imgflip.recent_memes_by_id[
        random.choice(imgflip.recent_memes_list)
    ]

    textExample = ""
    for i in range(randomTemplate["box_count"]):
        textExample += f"text{i+1}; "

    textExample = textExample.strip("; ")

    await m.message.edit(
        text=f"""
**Imgflip Meme generator module**

You can generate memes from the list of top 100 template provided from imgflip.com.

**Meme Generation Format:**
`@{(await c.get_me()).username} template text1; text2; text3; ...`

To see the available meme templates, tap 👉 /imgflip.
""",
        parse_mode="md",
        reply_markup=ikb(
            [
                [
                    (
                        "Example",
                        f"{randomTemplate['name']} {textExample}",
                        "switch_inline_query_current_chat",
                    )
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("^imgflipNav_(\d+)$"))
async def imgflipPage(c, m):
    page = int(m.data.split("_")[1])

    try:

        await m.message.edit_media(
            media=InputMediaPhoto(
                media="https://telegra.ph/file/9c7c7559dc455a700f25f.png",
                caption=f"Available Meme Templates",
                parse_mode="md",
            ),
            reply_markup=ikb(returnKeyboard(page)),
        )

    except bad_request_400.MessageNotModified:
        await m.answer(f"You are already on page {page}")


@Client.on_callback_query(filters.regex("^imgflipView_(\d+)_(\d+)$"))
async def imgflipView(c, m):

    templateID = str(m.data.split("_")[1])
    template = imgflip.recent_memes_by_id[templateID]

    page = int(m.data.split("_")[2])

    textExample = ""
    for i in range(template["box_count"]):
        textExample += f"text{i+1}; "

    textExample = textExample.strip("; ")

    keyboard = [
        [
            (
                "View Example",
                f"{template['name']} {textExample}",
                "switch_inline_query_current_chat",
            )
        ],
        [("Use this template", f"{template['name']} ", "switch_inline_query")],
        [
            (
                f"⏭️ {imgflip.recent_memes_by_id[imgflip.recent_memes_list[imgflip.recent_memes_list.index(template['id']) - 1]]['name'].replace('_', ' ').title()}",
                f"imgflipView_{imgflip.recent_memes_list[imgflip.recent_memes_list.index(template['id']) - 1]}_{page}",
            ),
            (
                f"⏭️ {imgflip.recent_memes_by_id[imgflip.recent_memes_list[imgflip.recent_memes_list.index(template['id']) + 1]]['name'].replace('_', ' ').title()}",
                f"imgflipView_{imgflip.recent_memes_list[imgflip.recent_memes_list.index(template['id']) + 1]}_{page}",
            ),
        ],
        [("Back 🔙", f"imgflipNav_{page}")],
    ]

    await m.message.edit_media(
        media=InputMediaPhoto(
            media=template["url"],
            caption=f"Template: **{template['name'].replace('_', ' ').title()}**\nInline Query: `{template['name']}`\nNumber of captions: **{template['box_count']}**",
            parse_mode="md",
        ),
        reply_markup=ikb(keyboard),
    )


############################################ Keyboard Definitions ############################################


def returnKeyboard(index=1, lines=5, columns=2):

    objects = imgflip.recent_memes_list

    page = Pagination(
        objects,
        page_data=page_data,  # callback to define the callback_data for page buttons in the bottom
        item_data=item_data,  # callback to define the callback_data for each item button
        item_title=item_title,  # callback to define the text for each item button
    )

    keyboard = page.create(index, lines, columns)

    return keyboard


def page_data(page):
    return f"imgflipNav_{page}"


def item_data(item, page):
    return f"imgflipView_{item}_{page}"


def item_title(item, page):
    return imgflip.recent_memes_by_id[item]["name"].replace("_", " ").title()

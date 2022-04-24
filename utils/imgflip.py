import requests

import configparser

config = configparser.ConfigParser()
config.read("config.ini")
creds = config["imgflip"]


async def createMeme(memeInfo, texts):

    param = {
        "username": creds["username"],
        "password": creds["password"],
        "template_id": memeInfo["id"],
    }

    if len(texts) == memeInfo["box_count"]:

        i = 0

        if memeInfo.get("boxes", False):

            for text in texts:

                # Using application/x-www-form-urlencoded encoded instead of JSON. https://stackoverflow.com/questions/66807028/error-message-when-using-boxes-with-imgflips-api

                param[f"boxes[{i}][text]"] = text
                param[f"boxes[{i}][x]"] = memeInfo["boxes"][i]["x"]
                param[f"boxes[{i}][y]"] = memeInfo["boxes"][i]["y"]
                param[f"boxes[{i}][width]"] = memeInfo["boxes"][i]["width"]
                param[f"boxes[{i}][height]"] = memeInfo["boxes"][i]["height"]

                i += 1

        else:

            for text in texts:
                param[f"boxes[{i}][text]"] = text
                i += 1

    else:

        raise Exception("Texts length does not match template length.")

    response = requests.request("POST", creds["url"], params=param).json()
    return response


def get_recent_memes_by_id():

    templates = {}

    response = requests.request("GET", "https://api.imgflip.com/get_memes").json()

    for meme in response["data"]["memes"]:

        formatted = {
            "id": meme["id"],
            "name": meme["name"].replace(" ", "_").replace("'", "").lower(),
            "url": meme["url"],
            "box_count": meme["box_count"],
        }

        templates.update({meme["id"]: formatted})

    return templates


def get_recent_memes_by_name():

    templates = {}

    response = requests.request("GET", "https://api.imgflip.com/get_memes").json()

    for meme in response["data"]["memes"]:

        formatted = {
            "id": meme["id"],
            "name": meme["name"].replace(" ", "_").replace("'", "").lower(),
            "url": meme["url"],
            "box_count": meme["box_count"],
        }

        templates.update(
            {meme["name"].replace(" ", "_").replace("'", "").lower(): formatted}
        )

    return templates


def cache_recent_memes():

    global recent_memes_by_id, recent_memes_by_name

    recent_memes_by_id = get_recent_memes_by_id()
    recent_memes_by_name = get_recent_memes_by_name()

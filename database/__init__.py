import asyncio
import motor.motor_asyncio


import configparser

config = configparser.ConfigParser()
config.read("config.ini")
database = config["database"]


import certifi

ca = certifi.where()


client = motor.motor_asyncio.AsyncIOMotorClient(database["uri"], tlsCAFile=ca)
db = client["meme-bot-v2"]

from pyrogram import Client


import os

configpresent = bool(os.path.exists("config.ini"))

if not configpresent:
    
    sampleconfig = open("sampleconfig.ini", "r").read()

    configtext = sampleconfig.format(
        
        api_id = os.environ.get('api_id'),
        api_hash = os.environ.get('api_hash'),
        api_token = os.environ.get('api_token'),
        uri = os.environ.get('uri'),
        db_name = os.environ.get('db_name'),
        sudo_users = os.environ.get('sudo_users'),
        sudo_chat = os.environ.get('sudo_chat'),
        log_chat = os.environ.get('log_chat'),
        #url = os.environ.get('imgflip_url'),
        username = os.environ.get('imgflip_username'),
        password = os.environ.get('imgflip_password'),
    )
    
    configfile = open("config.ini", "w")
    configfile.write(configtext)
    configfile.close()


import configparser
config = configparser.ConfigParser()
config.read('config.ini')
bot = config['tokens']


client = Client("bot", bot_token = str(bot['api_token']))
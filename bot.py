from client import client
from utils.imgflip import cache_recent_memes

cache_recent_memes()

print("[+] Starting bot...")
client.run()

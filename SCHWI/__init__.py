import asyncio
import time
import config
from pyrogram import Client, filters

loop = asyncio.get_event_loop()
boot = time.time()


botid = 0
botusername = ""
BOTID = 0
BOTUSERNAME = ""


from typing import Union
def cmd(comm: Union[list, str]):
  res = list()
  if isinstance(comm, str):
    res.extend([comm, f"{comm}@{botusername}"])
  if isinstance(comm, list):
    for com in comm:
      res.extend([com, f"{com}@{botusername}"])
  return filters.command(res, prefixes=["/", "?", "$", "!", "#", "@", ",", ".", "+", "~", "™", ";", ":", "-", "_"]) 

def parse_com(com, key):
  try:
    r = com.split(key,1)[1]
  except KeyError:
    return None
  r = (r.split(" ", 1)[1] if len(r.split()) >= 1 else None)
  return r

BOT1_TOKEN = "6265979983:AAHh0MVz9qRREziTedjvKUaT7E1DoCT0uGI"
BOT2_TOKEN = "6499811752:AAEuOKyeKmb0kltqE9rRiAQfUXXDJf7siSo"

app = Client(
    "LVLbot1",
    config.API_ID,
    config.API_HASH,
    bot_token=BOT1_TOKEN,
)

APP = Client(
    "LVLbot2",
    config.API_ID,
    config.API_HASH,
    bot_token=BOT2_TOKEN,
)

async def initiate_bot():
    global botid, botusername, BOTID, BOTUSERNAME
    await app.start()
    await APP.start()
    getme = await app.get_me()
    botid = getme.id
    botusername = (getme.username).lower()

    GETME = await APP.get_me()
    BOTID = GETME.id
    BOTUSERNAME = (GETME.username).lower()
    await APP.send_message(-1001986530465, "__BOT STARTED__ ✅")
    await app.send_message(-1001986530465, "__BOT STARTED__ ✅")




loop.run_until_complete(initiate_bot())

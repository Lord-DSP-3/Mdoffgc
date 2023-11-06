import asyncio
import time
import config
from pyrogram import Client, filters

loop = asyncio.get_event_loop()
boot = time.time()


botid = 0
botusername = ""

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

BOT1_TOKEN = "5721709783:AAHWao6d-4QYWBRzRpohYzHh6USUe9BWhrE"
STRING_SSS = ""

app = Client(
    "SecuritBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=BOT1_TOKEN,
)
bot = Client(
    "Securitadmin",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=STRING_SSS,
)

async def initiate_bot():
    global botid, botusername
    await app.start()
    await bot.start()
    getme = await app.get_me()
    botid = getme.id
    botusername = (getme.username).lower()


loop.run_until_complete(initiate_bot())

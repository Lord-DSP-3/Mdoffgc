import asyncio
import time
import config
from pyrogram import Client, filters



loop = asyncio.get_event_loop()
boot = time.time()


botid = 0
botname = ""
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

BOT1_TOKEN = "6265979983:AAHh0MVz9qRREziTedjvKUaT7E1DoCT0uGI"
BOT1_ID = 6265979983

app = Client(
    "LVLbot",
    config.API_ID,
    config.API_HASH,
    bot_token=BOT1_TOKEN,
)

async def initiate_bot():
    global botid, botname, botusername
    await app.start()
    getme = await app.get_me()
    botid = getme.id
    botusername = (getme.username).lower()
    if getme.last_name:
        botname = getme.first_name + " " + getme.last_name
    else:
        botname = getme.first_name


loop.run_until_complete(initiate_bot())

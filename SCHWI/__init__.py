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
STRING_1 = "AQC0CDUBYuZ2UedPT061vM1n56QALKuXAV9LsKQMIDm29fwfZ1RZRcJOgl3yH0cA757ZHt6Brj2VCg9M3C0RJkWLoyrEoQfQSqJ44L6rGeVGjrjZCLiMqFDTaBff-RgHFWAM8DDj-n1pW3MfCE-8H27lD3rZeoqahIAjLi4TbafO-YlwzFDbabIEgY64_CYNgO9CFK7JMbNhwJbZhNEXAexqrzhbZnhjyhYGgtVCKbBbma6D82whKQA97-nU0ZgCYV_Y7H-NF21_LFpTaLsJkWikhTDLHSlEwZyqS9Qg73PKdJBpETh_Uecx8SDZox1EIilDTAPEKIiy3LJJn0l8OlHKAAAAAT3iONIA"

app = Client(
    "LVLbot",
    config.API_ID,
    config.API_HASH,
    bot_token=BOT1_TOKEN,
)

bot = Client(
    name="userbot1",
    session_string=STRING_1,
    api_hash=config.API_HASH,
    api_id=config.API_ID
)

async def initiate_bot():
    global botid, botname, botusername
    await app.start()
    await bot.start()
    getme = await app.get_me()
    botid = getme.id
    botusername = (getme.username).lower()
    if getme.last_name:
        botname = getme.first_name + " " + getme.last_name
    else:
        botname = getme.first_name

loop.run_until_complete(initiate_bot())

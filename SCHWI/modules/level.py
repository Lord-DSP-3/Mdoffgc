from pyrogram import filters
import pymongo
from pymongo import MongoClient
from pyrogram.types import*

from SCHWI import app

#from Yukki.level_media import*
#from Yukki.level_name import*
from config import GROUP, MONGO_LEVEL_URI, ADMINS, BOT_USERNAME

levelnum = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100]


@bot.on_message(
    (filters.document
     | filters.text
     | filters.photo
     | filters.sticker
     | filters.animation
     | filters.video)
    & filters.chat(GROUP),
     group=100
)
async def level(client, message):
    user_id = message.from_user.id
    rtxt = "ㅤ"
    leveldb = MongoClient(MONGO_LEVEL_URI)
    level = leveldb["LEVEL"]["mem_LVL"]
    xpnum = level.find_one({"USER_ID": user_id})
    if not message.from_user.is_bot:
       if xpnum:
            xp = xpnum["xp"] + 1
            level.update_one({"USER_ID": user_id}, {
                "$set": {"xp": xp}})
            l = 0
            while True:
                if xp < ((125*(l**2))+(125*(l))):
                    break
                l += 1
            xp -= ((125*((l-1)**2))+(125*(l-1)))
            if xp == 0:
                for lv in range(len(levelname)) and range(len(levellink)):
                    if l == levelnum[lv]:
                        Link = f"{levellink[lv]}"
                        await message.reply_document(document=Link, caption=f"""
❯{message.from_user.mention}  __Reached Level__ {l}
❯Title: {levelname[lv]}
❯Check rank: /level
""", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Title ➫ More.info' , url="https://t.me/anime_chat_ranking_system")]]))
                    

REPU_EMOJI = ["❤️‍🔥", "🌟", "😼", "💕", "⭐", "💖"]
@bot.on_message(filters.text & filters.chat(GROUP) & filters.reply & filters.user(ADMINS), group=10)
async def add(_, message: Message):
    leveldb = MongoClient(MONGO_LEVEL_URI)
    level = leveldb["LEVEL"]["mem_LVL"]
    if message.text in REPU_EMOJI:
        member = message.reply_to_message.from_user.id
        admin = message.from_user.id
        k = level.find_one({"USER_ID": member})
        m = level.find_one({"USER_ID": admin})
        if k is None:
            await message.reply_to_message.reply_text(f"__To start your level mesure Click here👇🏻__\n[You need to start Bot in Private](https://t.me/{BOT_USERNAME}?start)", disable_web_page_preview=True)
        elif m is None:
            await message.reply_text(f"__To start your level mesure Click here👇🏻__\n[You need to start Bot in Private](https://t.me/{BOT_USERNAME}?start)", disable_web_page_preview=True)
        elif not member == admin and not message.reply_to_message.from_user.is_bot:
            am = m["Repu"]
            t = k["Repu"] + 1
            level.update_one({"USER_ID": member}, {
                "$set": {"Repu": t}})
            reputation = t
            await message.reply_to_message.reply_text(f"{message.from_user.mention} ({am} ✮) has increased Reputation for {message.reply_to_message.from_user.mention} ({t} ☆)↑↑")
      

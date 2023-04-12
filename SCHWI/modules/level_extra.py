import os
from pyrogram.types import*
from pyrogram import*
import pymongo
from pymongo import MongoClient
import random
from Yukki import app as bot, get_cmd
from config import MONGO_LEVEL_URI, ADMINS, GROUP, DEV, OWNER, MONGO_DB_URI


@bot.on_message(get_cmd("setrank") & filters.user(ADMINS) & filters.chat(GROUP))
async def rank(_, message: Message):
    leveldb = MongoClient(MONGO_LEVEL_URI)
    level = leveldb["LEVEL"]["mem_LVL"]
    if message.reply_to_message:
        member = message.reply_to_message.from_user.id
        sr = level.find_one({"USER_ID": member})
        if not message.reply_to_message.from_user.is_bot:
            if len(message.command) > 1:
                nrank = (message.text.split(None, 1)[1].strip())[:50]
                frtxt = f"𝚃𝙸𝚃𝙻𝙴:  {nrank}"
                level.update_one({"USER_ID": member}, {
                    "$set": {"trank": frtxt}})
                await message.reply_text(f"🎆Added Custom Rank \nUser: {message.reply_to_message.from_user.mention} \nTitle: {nrank}")
    else:
        await message.reply_text("__Bish Reply to user, who's rank you wanna set__")

@bot.on_message(get_cmd("status") & filters.user(ADMINS))
async def rank(client, message):
    leveldb = MongoClient(MONGO_LEVEL_URI)
    level = leveldb["LEVEL"]["mem_LVL"]
    if message.reply_to_message:
        midm = message.reply_to_message.from_user.mention
        mid = message.reply_to_message.from_user.id
        xpnum = level.find_one({"USER_ID": mid})
        xp = xpnum["xp"]
        rp = xpnum["Repu"]
        cs = xpnum["trank"]
        l = 0
        r = 0
        while True:
            if xp < ((125*(l**2))+(125*(l))):
                break
            l += 1
        xp -= ((125*((l-1)**2))+(125*(l-1)))
        rank = level.find().sort("xp", -1)
        fxp = f"{int(xp * 4)}/{int(2000 *((1/2) * l))}"
        for k in rank:
            r += 1
            if xpnum["USER_ID"] == k["USER_ID"]:
                break
        await message.reply_text(f"""
👤: {midm} ! `{mid}`
🛂: 
|-Level: {l} |-Rank: {r} |-Rep: {rp}
|-C{cs}  |-EXP: {fxp}
|-f.num: {xp}
""")
    else:
        await message.reply_text("__Bish Reply to user")


@bot.on_message(get_cmd("dellvldb") & filters.user(OWNER))
async def delone(_, message: Message):
    leveldb = MongoClient(MONGO_LEVEL_URI)
    level = leveldb["LEVEL"]["mem_LVL"]
    if len(message.command) != 1:
        uid = int(message.text.split(None, 1)[1])
        try:
            xpnum = level.delete_one({"USER_ID": uid})
            await message.reply_text("☑️")
        except Exception as e:
            await message.reply_text(e)

@bot.on_message(get_cmd("cleanlvldb") & filters.user(OWNER))
async def delmany(_, message: Message):
    leveldb = MongoClient(MONGO_LEVEL_URI)
    level = leveldb["LEVEL"]["mem_LVL"]
    try:
        xpnum = level.delete_many({"xp": 10})
        await message.reply_text("☑️")
    except Exception as e:
        await message.reply_text(e)

@bot.on_message(get_cmd("countlvldb") & filters.user(OWNER))
async def info_func(_, message: Message):
    leveldb = MongoClient(MONGO_LEVEL_URI)
    level = leveldb["LEVEL"]["mem_LVL"]
    try:
        count = level.count_documents({})
        await message.reply_text(f"TOTAL USERS IN DB : \n {count}")
    except Exception as e:
        await message.reply_text(e)

@bot.on_message(get_cmd("countxpdb") & filters.user(OWNER))
async def info_func(_, message: Message):
    leveldb = MongoClient(MONGO_LEVEL_URI)
    level = leveldb["LEVEL"]["mem_LVL"]
    try:
        count = level.count_documents({"xp": 10})
        await message.reply_text(f"TOTAL USERS with xp=10: \n {count}")
    except Exception as e:
        await message.reply_text(e)


@bot.on_message(get_cmd("add") & filters.user(DEV))
async def rank(_, message: Message):
    rpcli = MongoClient(MONGO_DB_URI)
    pymo = rpcli["R_PIC"]["PIC_DB"]
    reply = message.reply_to_message
    if reply.photo:
        picid = reply.photo.file_id
        picex = pymo.find_one({"PIC_ID": picid})
        if picex:
            await message.reply_text("Already existing Photo ID")
        else:
            newpic = {"PIC_ID": picid}
            pymo.insert_one(newpic)
            total_docs = pymo.count_documents({})
            await message.reply_text(f"✓ \n**+ {total_docs}**")
    else:
        await message.reply_text("Reply to a PNG file")
    
@bot.on_message(get_cmd("get") & filters.user(DEV))
async def rank(_, message: Message):
    rpcli = MongoClient(MONGO_DB_URI)
    pymo = rpcli["R_PIC"]["PIC_DB"]
    try:
        total_docs = pymo.count_documents({})
        random_index = random.randint(0, total_docs - 1)
        random_doc = pymo.find().skip(random_index).limit(1)[0]
        random_pic = random_doc["PIC_ID"]
        await message.reply_photo(random_pic)
    except Exception as e:
        await message.reply_text(e)

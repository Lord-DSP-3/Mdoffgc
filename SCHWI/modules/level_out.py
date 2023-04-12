from pyrogram import filters
import pymongo
from pymongo import MongoClient
import os
import random
from pyrogram.types import*

from Yukki import app as bot, get_cmd
from Yukki.level_name import*
from config import ADMINS, GROUP, MONGO_LEVEL_URI, BOT_USERNAME

levelnum = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100]
TT = [
    "💕",
    "❄️",
    "🦋",
    "Chotto matte kudasai...",
    "Matte matte kudasai...",
    "❣",
    "💜",
    "💚",
    "💛",
    "💙",
    "❤️",
]

async def get_user(user, already=False):
    user = await bot.get_users(user)
    mention = user.mention
    photo_id = user.photo.big_file_id if user.photo else None
    user_id = user.id

    leveldb = MongoClient(MONGO_LEVEL_URI)
    level = leveldb["LEVEL"]["mem_LVL"]
    xpnum = level.find_one({"USER_ID": user_id})
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
    for lv in range(len(levelname)):
        if l == levelnum[lv]:
            ilname = f"{levelname[lv]}"
            caption = f"""
╔────༻sᴛᴀᴛᴜs༺────╗
┣━👤 {mention}
┃  {cs}
┣━━━━━━━━━━━━━━━━┫
┣━⭐⁭𝑹𝑬𝑷𝑼𝑻𝑨𝑻𝑰𝑶𝑵: **{rp}**
┣𝙇𝙀𝙑𝙀𝙇: **{l}**
┣𝐑𝐀𝐍𝐊: **{r}** 🔝
┃ᴇxᴘ:  {fxp}
╚─────✩✯✰✯✩─────╝
"""
    return [caption, photo_id, ilname]


@bot.on_message(get_cmd(["myrank", "lvl", "level", "myprofile"]) & filters.chat(GROUP))
async def info_func(_, message: Message):
    user = message.from_user.id
    m = await message.reply_text(random.choice(TT))
    try:
        info_caption, photo_id, ilname = await get_user(user)
    except Exception as e:
        buttons = [[InlineKeyboardButton('Go  ➦' , url=f"https://t.me/{BOT_USERNAME}?start")]]
        return await m.edit(text=f"[You need to start Bot in Private](https://t.me/{BOT_USERNAME}?start=help) \n__To start your level mesure__", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
    if not photo_id:
        return await m.edit(info_caption, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f'{ilname}' , url="https://t.me/anime_chat_ranking_system")]]), disable_web_page_preview=True)
    photo = await bot.download_media(photo_id)
    await message.reply_document(document=photo, caption=info_caption, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f'{ilname}' , url="https://t.me/anime_chat_ranking_system")]]), quote=False)
    os.remove(photo)
    await m.delete()


@bot.on_message(get_cmd(["toplvl", "leaderboard", "toplevel"]) & filters.chat(GROUP))
async def topp(_, message: Message):
    tplvtx = await message.reply_text("💬")
    leveldb = MongoClient(MONGO_LEVEL_URI)
    level = leveldb["LEVEL"]["mem_LVL"]
    tl = level.find().sort("xp")
    if len(message.command) != 1:
        lmnt = int(message.text.split(None, 1)[1])
        dt1 = [x for x in level.find().sort('xp',pymongo.DESCENDING)][:lmnt]
    else:
        dt1 = [x for x in level.find().sort('xp',pymongo.DESCENDING)][:10]
    texto = "**⚜GROUP's TOP USERS LEADERBOARD**\n\n"
    num = 0
    for x in dt1:
        xp = x["xp"]
        rtxt = x["trank"]
        l = 0
        while True:
            if xp < ((125*(l**2))+(125*(l))):
                break
            l += 1
        xp -= ((125*((l-1)**2))+(125*(l-1)))
        fxp = f"{int(xp * 4)}/{int(2000 *((1/2) * l))}"
        try:
            users = await bot.get_users(x['USER_ID'])
            mention = users.first_name
        except Exception:
            mention = x['USER_ID']
        num += 1
        texto += f"{num}》{mention} ≛ 𝙇𝙚𝙫𝙚𝙡: **{l}** ᴇxᴘ: {fxp}\n     {rtxt}\n"
    try:
        await tplvtx.edit_text(texto)
    except Exception as e:
        await tplvtx.edit_text(e)

@bot.on_message(get_cmd(["toprep", "topreputaion"]) & filters.chat(GROUP))
async def topp(_, message: Message):
    tprptx = await message.reply_text("💬")
    leveldb = MongoClient(MONGO_LEVEL_URI)
    level = leveldb["LEVEL"]["mem_LVL"]
    tl = level.find().sort("Repu")
    if len(message.command) != 1:
        snmt = int(message.text.split(None, 1)[1])
        dt1 = [x for x in level.find().sort('Repu',pymongo.DESCENDING)][:snmt]
    else:
        dt1 = [x for x in level.find().sort('Repu',pymongo.DESCENDING)][:10]
    texto = "__GROUP's TOP REPUTATED MEMBERS__\n\n"
    num = 0
    for x in dt1:
        rp = x["Repu"]
        try:
            users = await bot.get_users(x['USER_ID'])
            mention = users.first_name
        except Exception:
            mention = x['USER_ID']
        num += 1
        texto += f"🔝{num} |-**⭐ {rp} ** ⟩ __{mention}__\n"
    await tprptx.edit_text(texto)

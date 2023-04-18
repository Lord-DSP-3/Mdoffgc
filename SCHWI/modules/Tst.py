from SCHWI import app as Bot
from pyrogram import Client, filters
from config import ADMINS
import pymongo, os

SUB_ANIME_DB = "mongodb+srv://lejah82077:7hDBz80lC4sKb7EN@cluster0.jo83ynu.mongodb.net/?retryWrites=true&w=majority"
DUB_ANIME_DB = "mongodb+srv://tasesey566:r7bEdOZnnE2lgL7H@cluster0.i17yfwi.mongodb.net/?retryWrites=true&w=majority"
PUBLIC_C_url = "https://t.me/HORNYSOCIETY18"
The_Other_Channel = "https://t.me/HORNYSOCIETY18"

dbclient1 = pymongo.MongoClient(SUB_ANIME_DB)
database1 = dbclient1["SUB_ANIME"]
sub_anime = database1['Anime_list']

async def present_sub_anime(anime_id : int):
    found = sub_anime.find_one({'_id': anime_id})
    return bool(found)

async def add_sub_anime(anime_id: int, link: str):
    sub_anime.insert_one({'_id': anime_id, '_link': link})
    return

async def full_sub_Animebase():
    user_docs = sub_anime.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_sub_anime(anime_id: int):
    sub_anime.delete_one({'_id': anime_id})
    return

async def get_sub_anime(anime_id : int):
    found = sub_anime.find_one({'_id': anime_id})
    dblink = found['_link']
    return dblink

@Bot.on_message(filters.command("addsub") & filters.user(ADMINS))
async def add_sub(client, message):
    if message.reply_to_message:
        link = message.reply_to_message.text
        if len(message.command) != 1:
            text = message.text.split(None, 1)[1]
            anime_id = int(text) 
            if not await present_sub_anime(anime_id):
                try:
                    await add_sub_anime(anime_id, link)
                    await message.reply_text(f"<b>ADDED!</b>\n\nID: <b>{anime_id}</b>\nLINK: {link}")
                except Exception as e:
                    await message.reply_text(f"An Error Occured//-\n\n{e}")
            else:
                dblink = await get_sub_anime(anime_id)
                await message.reply_text(f"<b>THIS ANIME ALREDY EXIST</b>\n\nID: <b>{anime_id}</b>\n<b>POST LINK:</b> {dblink}")
        else:
            await message.reply_text("<b>BISH PROVIDE ANIME ID AFTER COMMAND</b>\nTo Get Anime Id \nUse Command: /anime or /search")
    else:
        await message.reply_text(f"Bish Reply To Post Link From Channel:\n {PUBLIC_C_url}")
        
    
@Bot.on_message(filters.command("delsub") & filters.user(ADMINS))
async def add_sub(client, message):
    if len(message.command) != 1:
        text = message.text.split(None, 1)[1]
        anime_id = int(text) 
        if await present_sub_anime(anime_id):
            try:
                dblink = await get_sub_anime(anime_id)
                await del_sub_anime(anime_id)
                await message.reply_text(f"<b>DELETED!</b>\n\nID: <b>{anime_id}</b>\n<b>POST LINK:</b> {dblink}")
            except Exception as e:
                await message.reply_text(f"An Error Occured//-\n\n{e}")
        else:
            await message.reply_text(f"No Such Anime Was Inserted In DataBase With ID: {anime_id}")
    else:
        await message.reply_text("<b>BISH PROVIDE ANIME ID AFTER COMMAND</b>\nTo Get Anime Id \nUse Command: /anime or /search")

import requests
import random 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SCHWI import app


async def search_find_anime_list(anime_name: str):
    
    query = '''
        query ($search: String) {
            Page {
                media(search: $search, type: ANIME) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    status
                    bannerImage
                }
            }
        }
    '''
    variables = {"search": anime_name}
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})

   
    if response.status_code != 200:
        print("Api Error")
        return 
    
    data = response.json()["data"]
    anime_list = data["Page"]["media"]
    if not anime_list:
        print("Not Found")
        return

    banner_image = None
    if len(anime_list) == 1:
        banner_image = anime_list[0]["bannerImage"]
    else:
        banner_images = [anime["bannerImage"] for anime in anime_list if anime["bannerImage"]]
        if banner_images:
            banner_image = random.choice(banner_images)

    message_text = "TOP 4 SEARCH RESULTS:"
    buttons = []
    for i, anime in enumerate(anime_list[:4]):
        title = anime["title"]["english"] or anime["title"]["romaji"]
        anime_id = anime["id"]
        status = anime["status"]
        
        if status == "FINISHED":
            status_emoji = "🖥️"
        elif status == "RELEASING":
            status_emoji = "🆕"
        elif status == "NOT_YET_RELEASED":
            status_emoji = "🔜"
        elif status == "CANCELLED":
            status_emoji = "❌"
        elif status == "HIATUS":
            status_emoji = "🛑"
        elif status == "UPCOMING":
            status_emoji = "🎞️"
        else:
            status_emoji = ""
            
        buttons.append([InlineKeyboardButton(f"{status_emoji} {title}", callback_data=f"Anime_{anime_id}")])

    F_B = InlineKeyboardMarkup(buttons)
    return message_text, banner_image, F_B




@app.on_message(filters.command("anime"))
async def ani(client, message):
    H = message.chat.id
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Please provide an anime name or ID after the command")
        return

    arg = args[1]
    if arg.isdigit():
        anime_id = int(arg)
        await message.reply_text(f"Id: {anime_id}")
    else:
        anime_name = " ".join(args[1:])
        try:
            message_text, banner_image, F_B = await search_find_anime_list(anime_name)
            await app.send_photo(H, photo=banner_image, caption=message_text, reply_markup=F_B)
        except Exception as e:
            await message.reply_text(e)



















@app.on_message(filters.command("len"))
async def ln(client, message):

    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("<b>Please provide an anime name or ID after the command.</b>")
        return

    arg = args[1]
    if arg.isdigit():
        try:
            anime_id = int(arg)
        except Exception as e:
            await message.reply_text(e)
            return
        await message.reply_text(f'Int: {anime_id}')
    else:
        try:
            anime_name = " ".join(args[1:])
        except Exception as e:
            await message.reply_text(e)
        await message.reply_text(anime_name)



















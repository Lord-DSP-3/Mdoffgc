import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from SCHWI import app as bot

API_URL = "https://graphql.anilist.co"



@bot.on_message(filters.command("anime"))
def search_anime(client, message):
    """Search for anime on AniList and send possible results as a message with inline buttons."""
    query = message.text.split(" ", 1)[1]
    search_query = """
        query ($search: String) {
            Media (search: $search, type: ANIME) {
                id
                title {
                    romaji
                }
            }
        }
    """
    variables = {
        "search": query
    }
    response = requests.post(API_URL, json={"query": search_query, "variables": variables}).json()
    anime_list = response.get("data", {}).get("Media", [])
    if len(anime_list) == 0:
        message.reply_text("No anime found.")
        return
    results = []
    for anime in anime_list:
        title = anime.get("title", {}).get("romaji", "Unknown Title")
        anime_id = anime.get("id")
        results.append(
            InlineKeyboardButton(
                title=title,
                callback_data=f"anime_id:{anime_id}"
            )
        )
    reply_markup = InlineKeyboardMarkup([results])
    message.reply_text("Please select an anime:", reply_markup=reply_markup)

@bot.on_callback_query()
def send_anime_info(client, callback_query):
    """Send information about the selected anime."""
    anime_id = callback_query.data.split(":")[1]
    anime_query = """
        query ($id: Int) {
            Media (id: $id, type: ANIME) {
                id
                title {
                    romaji
                }
                coverImage {
                    medium
                }
                description
            }
        }
    """
    variables = {
        "id": int(anime_id)
    }
    response = requests.post(API_URL, json={"query": anime_query, "variables": variables}).json()
    anime_info = response.get("data", {}).get("Media")
    title = anime_info.get("title", {}).get("romaji", "Unknown Title")
    cover_image_url = anime_info.get("coverImage", {}).get("medium", None)
    description = anime_info.get("description", "No description available.")
    if cover_image_url is not None:
        cover_image_data = requests.get(cover_image_url).content
        cover_image_file = f"cover_image_{anime_id}.jpg"
        with open(cover_image_file, "wb") as f:
            f.write(cover_image_data)
        caption = f"<b>{title}</b>\n\n{description}"
        callback_query.message.reply_photo(photo=cover_image_file, caption=caption, parse_mode="html")
        os.remove(cover_image_file)
    else:
        callback_query.answer("No cover image found for this anime.", show_alert=True)



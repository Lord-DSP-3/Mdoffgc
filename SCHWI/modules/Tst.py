from SCHWI import app as bot
from pyrogram import Client, filters
import requests

# Command to get anime info
@bot.on_message(filters.command(["anime"]))
async def anime_info(client, message):
    # Get the AniList ID from the command arguments
    args = message.text.split()
    if len(args) < 2:
        message.reply_text("Please provide an AniList ID.")
        return
    anime_id = args[1]
    
    # Build the AniList API query URL
    query = '''
    query ($id: Int) {
        Media (id: $id, type: ANIME) {
            id
            title {
                romaji
                english
                native
            }
            format
            status
            episodes
            duration
            genres
            averageScore
            description
            coverImage {
                medium
            }
        }
    }
    '''
    variables = {"id": anime_id}
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})

    # Check if the API request was successful
    if response.status_code != 200:
        message.reply_text("Failed to get anime info.")
        return
    
    # Parse the API response and format the message
    anime = response.json()["data"]["Media"]
    title = anime["title"]["english"] or anime["title"]["romaji"]
    status = anime["status"]
    format = anime["format"]
    episodes = anime["episodes"]
    duration = anime["duration"]
    genres = ", ".join(anime["genres"])
    score = anime["averageScore"]
    description = anime["description"]
    cover_image = anime["coverImage"]["medium"]
    
    message_text = f"<b>{title}</b>\n"\
                   f"<b>Status:</b> {status}\n"\
                   f"<b>Format:</b> {format}\n"\
                   f"<b>Episodes:</b> {episodes}\n"\
                   f"<b>Duration:</b> {duration} min.\n"\
                   f"<b>Genres:</b> {genres}\n"\
                   f"<b>Score:</b> {score}/100\n"\
                   f"<b>Description:</b> {description}"
    
    await message.reply_photo(photo=cover_image, caption=message_text)

 

# Command to search for an anime and get its info
@bot.on_message(filters.command(["search_anime"]))
async def search_anime(client, message):
    # Get the anime name from the command arguments
    args = message.text.split()
    if len(args) < 2:
        message.reply_text("Please provide an anime name.")
        return
    anime_name = " ".join(args[1:])

    # Build the AniList API query URL
    query = '''
    query ($search: String) {
        Media (search: $search, type: ANIME) {
            id
            title {
                romaji
                english
                native
            }
            format
            status
            episodes
            duration
            genres
            averageScore
            description
            coverImage {
                medium
            }
        }
    }
    '''
    variables = {"search": anime_name}
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})

    # Check if the API request was successful
    if response.status_code != 200:
        message.reply_text("Failed to get anime info.")
        return
    
    # Parse the API response and format the message
    data = response.json()["data"]
    if not data["Media"]:
        message.reply_text(f"No anime found with the name '{anime_name}'.")
        return
    
    anime = data["Media"][0]
    title = anime["title"]["english"] or anime["title"]["romaji"]
    anime_id = anime["id"]
    status = anime["status"]
    format = anime["format"]
    episodes = anime["episodes"]
    duration = anime["duration"]
    genres = ", ".join(anime["genres"])
    score = anime["averageScore"]
    description = anime["description"]
    cover_image = anime["coverImage"]["medium"]
    
    message_text = f"<b>{title}</b>\n"\
                   f"<b>AniList ID:</b> {anime_id}\n"\
                   f"<b>Status:</b> {status}\n"\
                   f"<b>Format:</b> {format}\n"\
                   f"<b>Episodes:</b> {episodes}\n"\
                   f"<b>Duration:</b> {duration} min.\n"\
                   f"<b>Genres:</b> {genres}\n"\
                   f"<b>Score:</b> {score}/100\n"\
                   f"<b>Description:</b> {description}\n"\
                   f"<b>Cover Image:</b> {cover_image}"
    
    await message.reply_text(message_text)





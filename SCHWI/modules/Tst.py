from SCHWI import app as bot
from pyrogram import Client, filters
import requests

# Command to get anime info
@bot.on_message(filters.command(["anime"]))
def anime_info(client, message):
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
                   f"<b>Description:</b> {description}\n"\
                   f"<b>Cover Image:</b> {cover_image}"
    
    await message.reply_text(message_text)


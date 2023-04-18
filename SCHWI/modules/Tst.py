from SCHWI import app as bot
from pyrogram import Client, filters
import requests

# Command to search for an anime and get its info
@bot.on_message(filters.command(["search"]))
def search_anime(client, message):
    # Get the anime name from the command arguments
    args = message.text.split()
    if len(args) < 2:
        message.reply_text("Please provide an anime name.")
        return
    anime_name = " ".join(args[1:])

    # Build the AniList API query URL
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
    anime_list = data["Page"]["media"]
    if not anime_list:
        message.reply_text(f"No anime found with the name '{anime_name}'.")
        return

    # Build the list of search results
    message_text = f"Top 5 search results for '{anime_name}':\n\n"
    for i, anime in enumerate(anime_list[:10]):
        title = anime["title"]["english"] or anime["title"]["romaji"]
        anime_id = anime["id"]
        message_text += f"🖥️{i+1}. {title} (ID: {anime_id})\n\n"

    message.reply_text(message_text)

from pyrogram import Client, filters
import requests

# Replace "YOUR_BOT_TOKEN" with your actual bot token
bot = Client("my_bot", bot_token="YOUR_BOT_TOKEN")

# Command to get anime info by ID
@bot.on_message(filters.command(["anime_info"]))
def anime_info(client, message):
    # Get the anime ID from the command arguments
    args = message.text.split()
    if len(args) < 2:
        message.reply_text("Please provide an anime ID.")
        return
    anime_id = int(args[1])

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
            coverImage {
                extraLarge
            }
            description
            format
            episodes
            status
            genres
            averageScore
            studios(isMain: true) {
                edges {
                    node {
                        name
                    }
                }
            }
            startDate {
                year
                month
                day
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
    data = response.json()["data"]
    anime = data["Media"]
    if not anime:
        message.reply_text(f"No anime found with the ID '{anime_id}'.")
        return

    title = anime["title"]["english"] or anime["title"]["romaji"]
    cover_url = anime["coverImage"]["extraLarge"]
    description = anime["description"]
    format = anime["format"]
    episodes = anime["episodes"]
    status = anime["status"]
    genres = ", ".join(anime["genres"])
    average_score = anime["averageScore"]
    studio = anime["studios"]["edges"][0]["node"]["name"]
    start_date = f"{anime['startDate']['day']}/{anime['startDate']['month']}/{anime['startDate']['year']}"

    message_text = f"<b>{title}</b>\n"
    message_text += f"<i>{studio} - {start_date}</i>\n"
    message_text += f"<b>Genres:</b> {genres}\n\n"
    message_text += f"<b>Average Score:</b> {average_score}/100\n\n"
    message_text += f"{description}"

    message.reply_photo(cover_url, caption=message_text, parse_mode="HTML")



# Command to get anime info by ID
@bot.on_message(filters.command(["anime"]))
def anime_info(client, message):
    # Get the anime ID from the command arguments
    args = message.text.split()
    if len(args) < 2:
        message.reply_text("Please provide an anime ID.")
        return
    anime_id = int(args[1])

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
            coverImage {
                extraLarge
            }
            description
            format
            episodes
            status
            genres
            averageScore
            studios(isMain: true) {
                edges {
                    node {
                        name
                    }
                }
            }
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            duration
            season
            seasonYear
            trailer {
                id
                site
                thumbnail
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
    data = response.json()["data"]
    anime = data["Media"]
    if not anime:
        message.reply_text(f"No anime found with the ID '{anime_id}'.")
        return

    title = anime["title"]["english"] or anime["title"]["romaji"]
    cover_url = anime["coverImage"]["extraLarge"]
    description = anime["description"]
    format = anime["format"]
    episodes = anime["episodes"]
    status = anime["status"]
    genres = ", ".join(anime["genres"])
    average_score = anime["averageScore"]
    studio = anime["studios"]["edges"][0]["node"]["name"]
    start_date = f"{anime['startDate']['day']}/{anime['startDate']['month']}/{anime['startDate']['year']}"
    end_date = f"{anime['endDate']['day']}/{anime['endDate']['month']}/{anime['endDate']['year']}" if anime['endDate'] else ""
    duration = f"{anime['duration']} mins" if anime['duration'] else ""
    season = f"{anime['season']} {anime['seasonYear']}" if anime['season'] else ""
    trailer_url = f"https://www.youtube.com/watch?v={anime['trailer']['id']}" if anime['trailer'] else ""

    message_text = f"<b>{title}</b>\n"
    message_text += f"<i>{studio} - {start_date} to {end_date}</i>\n"
    message_text += f"<b>Genres:</b> {genres}\n"
    message_text += f"<b>Format:</b> {format}\n"
    message_text += f"<b>Episodes:</b> {episodes} Duration: {duration}\n"
    message_text += f"<b>Status:</b> {status}\n"
    message_text += f"<b>Average Score:</b> {average_score}\n"
    message_text += f"Season {season}\n"
    message_text += f"Start: {start_date}  End {end_date} \n\n"
    message_text += f"DESCRIPTION: {description}"

    message.reply_text(message_text)
    message.reply_photo(cover_url, caption=message_text)

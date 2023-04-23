import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SCHWI import app

# Define the /anime command
@app.on_message(filters.command("anime"))
def anime_search(client, message):

    args = message.text.split()
    if len(args) < 2:
    await message.reply_text("<b>Please provide an anime name or ID after the command.</b>")
    return

    arg = args[1]
    if arg.isdigit():
        anime_id = int(arg)
    else:
        string = arg

    # Set up the query to send to the AniList API
    search_query = '''
    query ($search: String) {
      Media(search: $search, type: ANIME, sort: SEARCH_MATCH) {
        id
        title {
          romaji
        }
      }
    }
    '''

    # Set up the query variables with the user's search query
    variables = {
        'search': query
    }

    # Send the query to the AniList API and get the response
    response = requests.post(search_url, json={'query': search_query, 'variables': variables}, headers={'Authorization': f'Bearer {access_token}'})

    # Parse the response and get the top 4 matching anime
    anime_list = response.json()['data']['Media']['title']
    anime_results = []
    for anime in anime_list[:4]:
        anime_id = response.json()['data']['Media']['id']
        anime_title = anime['romaji']
        anime_results.append(f"{anime_title} (ID: {anime_id})")

    # Send the results back to the user
    if anime_results:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(f"Watch {anime_results[0]}", url=f"https://anilist.co/anime/{anime_id}")]])
        message.reply_text(f"Here are the top 4 results for '{query}':\n\n" + "\n".join(anime_results), reply_markup=reply_markup)
    else:
        message.reply_text("Sorry, no results found for your query.")

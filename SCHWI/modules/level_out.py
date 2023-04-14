from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from SCHWI import app
import random
from string import hexdigits
cache = dict()
import requests
import urllib.parse

emoji = "🖥"


class AnimeDex:
    def __init__(self) -> None:
        pass

    def search(query):
        url = 'https://animedex.live/search?query=' + \
            str(urllib.parse.quote(query))
        soup = bs(requests.get(url).content, 'html.parser')
        animes = []

        for anime in soup.find('div', 'divox').find_all('a'):
            title = anime.find('h3').text
            url = 'https://animedex.live' + anime.get('href')
            animes.append((title, url))
        return animes

    def anime(url):
        soup = bs(requests.get(url).content, 'html.parser')

        title = soup.find('h1').text
        text = f'{emoji()} **{title}**\n'
        img = soup.find('div', 'poster').find('img').get('src')

        item = soup.find_all('div', 'info-items')[2:-1]
        for i in item:
            text += '\n' + i.text.strip().replace('\n', ' ')

        genres = soup.find('div', 'info-items genre').find_all('a')
        text += '\nGenres: '
        for i in genres:
            text += i.text + ', '
        text = text[:-2]

        ep = []
        eps = soup.find_all('a', 'ep-btn')
        for i in eps:
            ep.append((i.text, 'https://animedex.live' + i.get('href')))

        return img, text, ep

    def episode(url):
        soup = bs(requests.get(url).content, 'html.parser')
        text = soup.find('b').text

        sub = soup.find('div', 'server').find_all('div', 'sitem')
        surl = []
        for i in sub:
            url = 'https://animedex.live' + \
                i.find('a').get('data-value').split(' ')[0]
            surl.append((i.text.strip(), url))

        dub = soup.find('div', 'server sd')
        durl = []
        if dub:
            for i in dub.find_all('div', 'sitem'):
                url = 'https://animedex.live' + \
                    i.find('a').get('data-value').split(' ')[0]
                durl.append((i.text.strip(), url))

        return text, surl, durl





def get_hash(data, back):
    while True:
        hash = ''.join(random.choices(hexdigits, k=10))
        if not cache.get(hash):
            cache[hash] = (data, back)
            break
    return hash


def get_hash_btn(data: None, hash: None):
    if hash:
        cache[hash] = data
        return hash

    if not data:
        while True:
            hash = ''.join(random.choices(hexdigits, k=10))
            if not cache.get(hash):
                cache[hash] = ''
                break
    else:
        while True:
            hash = ''.join(random.choices(hexdigits, k=10))
            if not cache.get(hash):
                cache[hash] = data
                break
    return hash


def get_hash_anime(data):
    while True:
        hash = ''.join(random.choices(hexdigits, k=10))
        if not cache.get(hash):
            cache[hash] = data
            break
    return hash


class BTN:
    def searchCMD(id, data, back):
        temp = []
        pos = 1
        x = []

        for i in data:
            cb = f'AnimeS {id} ' + get_hash(i[1], back)
            temp.append([
                InlineKeyboardButton(text=i[0], callback_data=cb)]
            )
        pos = len(temp)
        hash = get_hash_btn(None, None)

        if len(temp) > 10:
            b_parts = []
            x = 0
            page = 0

            while pos > 10:
                t = temp[x:x+10]

                if len(t) == 0:
                    break
                b_parts.append(t)
                x += 10
                pos -= 10

                if page == 0:
                    b_parts[page].append([
                        InlineKeyboardButton(
                            text='Next  ⫸', callback_data=f'switch_anime {id} {hash} 1')
                    ])
                else:
                    b_parts[page].append(
                        [
                            InlineKeyboardButton(
                                text='⫷ Prev', callback_data=f'switch_anime {id} {hash} {page-1}'),
                            InlineKeyboardButton(
                                text='Next ⫸', callback_data=f'switch_anime {id} {hash} {page+1}')
                        ])

                page += 1
            if pos > 0:
                b_parts.append(temp[x:])
                b_parts[page].append(
                    [
                        InlineKeyboardButton(
                            text='⫷ Prev', callback_data=f'switch_anime {id} {hash} {page-1}')
                    ])

            hash = get_hash_btn((b_parts, back), hash)
            BTN = b_parts[0]
            return InlineKeyboardMarkup(BTN)
        else:
            return InlineKeyboardMarkup(temp)

    def AnimeS(id, data, back):
        temp = []
        pos = 1
        x = []

        for i in data:
            cb = f'episode {id} ' + get_hash(i[1], back)
            if pos % 4 == 0:
                x.append(
                    InlineKeyboardButton(text=i[0], callback_data=cb)
                )
                temp.append(x)
                x = []
            else:
                x.append(
                    InlineKeyboardButton(text=i[0], callback_data=cb)
                )
            pos += 1

        if len(x) != 0:
            temp.append(x)

        hash = get_hash_btn(None, None)

        if len(temp) > 23:
            b_parts = []
            x = 0
            page = 0

            while pos > 23:
                t = temp[x:x+23]

                if len(t) == 0:
                    break
                b_parts.append(t)
                x += 23
                pos -= 23

                if page == 0:
                    b_parts[page].append([
                        InlineKeyboardButton(
                            text='Back', callback_data=f'searchBACK {id} {back}'),
                        InlineKeyboardButton(
                            text='Next  ⫸', callback_data=f'switch_ep {id} {hash} 1')
                    ])
                else:
                    b_parts[page].append(
                        [
                            InlineKeyboardButton(
                                text='⫷ Prev', callback_data=f'switch_ep {id} {hash} {page-1}'),
                            InlineKeyboardButton(
                                text='Next ⫸', callback_data=f'switch_ep {id} {hash} {page+1}')
                        ])
                b_parts[page].append(
                    [
                        InlineKeyboardButton(
                            text='Back', callback_data=f'searchBACK {id} {back}')
                    ]
                )
                page += 1
            if pos > 0:
                b_parts.append(temp[x:])
                b_parts[page].append(
                    [
                        InlineKeyboardButton(
                            text='⫷ Prev', callback_data=f'switch_ep {id} {hash} {page-1}'),
                        InlineKeyboardButton(
                            text='Back', callback_data=f'searchBACK {id} {back}')
                    ])

            hash = get_hash_btn((b_parts, back), hash)
            BTN = b_parts[0]
            return InlineKeyboardMarkup(BTN)
        else:
            temp.append([InlineKeyboardButton(
                text='Back', callback_data=f'searchBACK {id} {back}')])
            return InlineKeyboardMarkup(temp)

    def episode(id, surl, durl, back):
        temp = []
        pos = 1
        x = []
        temp.append([InlineKeyboardButton(
            text='⬇️ English Subbed ⬇️', callback_data='engSUB')])

        for i in surl:
            if pos % 3 == 0:
                x.append(
                    InlineKeyboardButton(text=i[0], url=i[1])
                )
                temp.append(x)
                x = []
            else:
                x.append(
                    InlineKeyboardButton(text=i[0], url=i[1])
                )
            pos += 1

        if len(x) != 0:
            temp.append(x)

        if len(durl) != 0:
            temp.append([InlineKeyboardButton(
                text='➖➖➖➖➖➖➖➖➖➖', callback_data='line')])

            temp.append([InlineKeyboardButton(
                text='⬇️ English Dubbed ⬇️', callback_data='engDUB')])

            for i in durl:
                if pos % 3 == 0:
                    x.append(
                        InlineKeyboardButton(text=i[0], url=i[1])
                    )
                    temp.append(x)
                    x = []
                else:
                    x.append(
                        InlineKeyboardButton(text=i[0], url=i[1])
                    )
                pos += 1

            if len(x) != 0:
                temp.append(x)
        temp.append([InlineKeyboardButton(
            text='Back', callback_data=f'AnimeS {id} {back}')])
        return InlineKeyboardMarkup(temp)


QUERY = '**Search Results:** `{}`'

@app.on_message(filters.command(['search', 's']))
async def searchCMD(_, message: Message):
    try:
        user = message.from_user.id
        query = ' '.join(message.command[1:])
        if query == '':
            return await message.reply_text('Give me something to search ^_^')
        data = AnimeDex.search(query)
        button = BTN.searchCMD(user, data, query)
        await message.reply_text(QUERY.format(query), reply_markup=button)
    except Exception as e:
        try:
            return await message.reply_text('**Anime Not Found...**\n\nProbably Incorrect Name, Try again')
        except:
            return

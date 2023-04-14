import asyncio
from types import NoneType
import requests
import time
import random
import re
import os
from pyrogram import*
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import*
from pyrogram.errors import UserNotParticipant, WebpageCurlFailed, WebpageMediaEmpty


failed_pic = "https://telegra.ph/file/09733b49f3a9d5b147d21.png"
PIC_LS  = [
    'https://telegra.ph/file/0d2097f442e816ba3f946.jpg',
    'https://telegra.ph/file/5a152016056308ef63226.jpg',
    'https://telegra.ph/file/d2bf913b18688c59828e9.jpg',
    'https://telegra.ph/file/d53083ea69e84e3b54735.jpg',
    'https://telegra.ph/file/b5eb1e3606b7d2f1b491f.jpg'
]

def get_btns(
    media,
    user: int,
    result: list,
    lsqry: str = None,
    lspage: int = None,
    auth: bool = False,
    sfw: str = "False"
):
    buttons = []
    qry = f"_{lsqry}" if lsqry is not None else ""
    pg = f"_{lspage}" if lspage is not None else ""
    if media == "ANIME" and sfw == "False":
        buttons.append([
            InlineKeyboardButton(
                text="Characters",
                callback_data=(
                    f"char_{result[2][0]}_ANI"
                    +f"{qry}{pg}_{str(auth)}_1_{user}"
                )
            ),
            InlineKeyboardButton(
                text="Description",
                callback_data=(
                    f"desc_{result[2][0]}_ANI"
                    +f"{qry}{pg}_{str(auth)}_{user}"
                )
            ),
            InlineKeyboardButton(
                text="List Series",
                callback_data=(
                    f"ls_{result[2][0]}_ANI"
                    +f"{qry}{pg}_{str(auth)}_{user}"
                )
            ),
        ])
    if media == "CHARACTER":
        buttons.append([
            InlineKeyboardButton(
                "Description",
                callback_data=(
                    f"desc_{result[2][0]}_CHAR"
                    +f"{qry}{pg}_{str(auth)}_{user}"
                )
            )
        ])
        buttons.append([
            InlineKeyboardButton(
                "List Series",
                callback_data=f"lsc_{result[2][0]}{qry}{pg}_{str(auth)}_{user}"
            )
        ])
    if media == "SCHEDULED":
        if result[0]!=0 and result[0]!=6:
            buttons.append([
                InlineKeyboardButton(
                    str(day_(result[0]-1)),
                    callback_data=f"sched_{result[0]-1}_{user}"
                ),
                InlineKeyboardButton(
                    str(day_(result[0]+1)),
                    callback_data=f"sched_{result[0]+1}_{user}"
                )
            ])
        if result[0] == 0:
            buttons.append([
                InlineKeyboardButton(
                    str(day_(result[0]+1)),
                    callback_data=f"sched_{result[0]+1}_{user}"
                )
            ])
        if result[0] == 6:
            buttons.append([
                InlineKeyboardButton(
                    str(day_(result[0]-1)),
                    callback_data=f"sched_{result[0]-1}_{user}"
                )
            ])
    if media == "MANGA" and sfw == "False":
        buttons.append([
            InlineKeyboardButton("More Info", url=result[1][2])
        ])
    if media == "AIRING" and sfw == "False":
        buttons.append([
            InlineKeyboardButton("More Info", url=result[1][0])
        ])
    if auth is True and media!="SCHEDULED" and sfw == "False":
        auth_btns = get_auth_btns(
            media,user, result[2], lspage=lspage, lsqry=lsqry
        )
        buttons.append(auth_btns)
    if len(result)>3:
        if result[3] == "None":
            if result[4] != "None":
                buttons.append([
                    InlineKeyboardButton(
                        text="Sequel",
                        callback_data=f"btn_{result[4]}_{str(auth)}_{user}"
                    )
                ])
        else:
            if result[4] != "None":
                buttons.append([
                    InlineKeyboardButton(
                        text="Prequel",
                        callback_data=f"btn_{result[3]}_{str(auth)}_{user}"
                    ),
                    InlineKeyboardButton(
                        text="Sequel",
                        callback_data=f"btn_{result[4]}_{str(auth)}_{user}"
                    ),
                ])
            else:
                buttons.append([
                    InlineKeyboardButton(
                        text="Prequel",
                        callback_data=f"btn_{result[3]}_{str(auth)}_{user}"
                    )
                ])
    if (lsqry is not None) and (len(result)!=1):
        if lspage==1:
            if result[1][1] is True:
                buttons.append([
                    InlineKeyboardButton(
                        text="Next",
                        callback_data=(
                            f"page_{media}{qry}_{int(lspage)+1}_{str(auth)}_{user}"
                        )
                    )
                ])
            else:
                pass
        elif lspage!=1:
            if result[1][1] is False:
                buttons.append([
                    InlineKeyboardButton(
                        text="Prev",
                        callback_data=(
                            f"page_{media}{qry}_{int(lspage)-1}_{str(auth)}_{user}"
                        )
                    )
                ])
            else:
                buttons.append([
                    InlineKeyboardButton(
                        text="Prev",
                        callback_data=(
                            f"page_{media}{qry}_{int(lspage)-1}_{str(auth)}_{user}"
                        )
                    ),
                    InlineKeyboardButton(
                        text="Next",
                        callback_data=(
                            f"page_{media}{qry}_{int(lspage)+1}_{str(auth)}_{user}"
                        )
                    )
                ])
    return InlineKeyboardMarkup(buttons)

ANIME_QUERY = """
query ($id: Int, $idMal:Int, $search: String) {
    Media (id: $id, idMal: $idMal, search: $search, type: ANIME) {
        id
        idMal
        title {
            romaji
            english
            native
        }
        format
        status
        episodes
        duration
        countryOfOrigin
        source (version: 2)
        trailer {
            id
            site
        }
        genres
        tags {
            name
        }
        averageScore
        relations {
            edges {
                node {
                    title {
                        romaji
                        english
                    }
                    id
                    type
                }
                relationType
            }
        }
        nextAiringEpisode {
            timeUntilAiring
            episode
        }
        isAdult
        isFavourite
        mediaListEntry {
            status
            score
            id
        }
        siteUrl
    }
}
"""
async def return_json_senpai(
    query: str,
    vars_: dict,
    auth: bool = False,
    user: int = None
):
    url = "https://graphql.anilist.co"
    headers = None
    if auth:
        headers = {
            'Authorization': (
                'Bearer ' 
                +str((await AUTH_USERS.find_one({"id": int(user)}))['token'])
            ),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
    return requests.post(
        url,
        json={"query": query, "variables": vars_},
        headers=headers
    ).json()

BOT_NAME = "MCAHN"

def make_it_rw(time_stamp):
    """Converting Time Stamp to Readable Format"""
    seconds, milliseconds = divmod(int(time_stamp), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " Days, ") if days else "")
        + ((str(hours) + " Hours, ") if hours else "")
        + ((str(minutes) + " Minutes, ") if minutes else "")
        + ((str(seconds) + " Seconds, ") if seconds else "")
        + ((str(milliseconds) + " ms, ") if milliseconds else "")
    )
    return tmp[:-2]

def pos_no(no):
    ep_ = list(str(no))
    x = ep_.pop()
    if ep_ != [] and ep_.pop()=='1':
        return 'th'
    th = (
        "st" if x == "1" 
        else "nd" if x == "2" 
        else "rd" if x == "3" 
        else "th"
    )
    return th

ANIME_TEMPLATE = """{name}
**ID | MAL ID:** `{idm}` | `{idmal}`
{bl}**{psrc}:** `{source}`
{bl}**{ptype}:** `{formats}`{avscd}{dura}{user_data}
{status_air}{gnrs_}{tags_}
🎬 {trailer_link}
📖 <a href="{surl}">Synopsis</a>
📖 <a href="{url}">Official Site</a>
<a href="https://t.me/{bot}?start=anirec_{idm}">Recommendations</a>
{additional}"""


async def get_anime(
    vars_,
    auth: bool = False,
    user: int = None,
    cid: int = None
):
    result = await return_json_senpai(
        ANIME_QUERY, vars_, auth=auth, user=user
    )

    error = result.get("errors")
    if error:
        error_sts = error[0].get("message")
        return [f"[{error_sts}]"]

    data = result["data"]["Media"]

    # Data of all fields in returned json
    # pylint: disable=possibly-unused-variable
    idm = data.get("id")
    idmal = data.get("idMal")
    romaji = data["title"]["romaji"]
    english = data["title"]["english"]
    native = data["title"]["native"]
    formats = data.get("format")
    status = data.get("status")
    episodes = data.get("episodes")
    duration = data.get("duration")
    country = data.get("countryOfOrigin")
    c_flag = cflag(country)
    source = data.get("source")
    prqlsql = data.get("relations").get("edges")
    adult = data.get("isAdult")
    url = data.get("siteUrl")
    trailer_link = "N/A"
    gnrs = ", ".join(data['genres'])
    score = data['averageScore']
    bl, cs = await uidata(cid)
    text = await get_ui_text(cs)
    psrc, ptype = text[0], text[1]
    avscd = (
        f"\n{bl}**{text[2]}:** `{score}%` 🌟" if score is not None
        else ""
    )
    tags = []
    for i in data['tags']:
        tags.append(i["name"])
    tags_ = (
        f"\n{bl}**{text[8]}:** `{', '.join(tags[:5])}`" if tags != []
        else ""
    )
    bot = BOT_NAME.replace("@", "")
    gnrs_ = ""
    if len(gnrs)!=0:
        gnrs_ = f"\n{bl}**{text[7]}:** `{gnrs}`"
    isfav = data.get("isFavourite")
    fav = ", in Favourites" if isfav is True else ""
    user_data = ""
    in_ls = False
    in_ls_id = ""
    if auth is True:
        in_list = data.get("mediaListEntry")
        if in_list is not None:
            in_ls = True
            in_ls_id = in_list['id']
            in_ls_stts = in_list['status']
            in_ls_score = (
                f" and scored {in_list['score']}" if in_list['score']!=0
                else ""
            )
            user_data = (
                f"\n{bl}**{text[4]}:** `{in_ls_stts}{fav}{in_ls_score}`"
            )
    if data["title"]["english"] is not None:
        name = f"""[{c_flag}]**{romaji}**
        __{english}__
        {native}"""
    else:
        name = f"""[{c_flag}]**{romaji}**
        {native}"""
    prql, prql_id, sql, sql_id = "", "None", "", "None"
    for i in prqlsql:
        if i["relationType"] == "PREQUEL" and i["node"]["type"]=="ANIME":
            pname = (
                i["node"]["title"]["english"]
                if i["node"]["title"]["english"] is not None
                else i["node"]["title"]["romaji"]
            )
            prql += f"**{text[10]}:** `{pname}`\n"
            prql_id = i["node"]["id"]
            break
    for i in prqlsql:
        if i["relationType"] == "SEQUEL" and i["node"]["type"]=="ANIME":
            sname = (
                i["node"]["title"]["english"]
                if i["node"]["title"]["english"] is not None
                else i["node"]["title"]["romaji"]
            )
            sql += f"**{text[9]}:** `{sname}`\n"
            sql_id = i["node"]["id"]
            break
    additional = f"{prql}{sql}"
    surl = f"https://t.me/{bot}/?start=des_ANI_{idm}_desc"
    dura = (
        f"\n{bl}**{text[3]}:** `{duration} min/ep`"
        if duration is not None
        else ""
    )
    air_on = None
    if data["nextAiringEpisode"]:
        nextAir = data["nextAiringEpisode"]["timeUntilAiring"]
        air_on = make_it_rw(nextAir*1000)
        eps = data["nextAiringEpisode"]["episode"]
        th = pos_no(str(eps))
        air_on += f" | {eps}{th} eps"
    if air_on is None:
        eps_ = f"` | `{episodes} eps" if episodes is not None else ""
        status_air = f"{bl}**{text[6]}:** `{status}{eps_}`"
    else:
        status_air = (
            f"{bl}**{text[6]}:** `{status}`\n{bl}**{text[11]}:** `{air_on}`"
        )
    if data["trailer"] and data["trailer"]["site"] == "youtube":
        trailer_link = (
            f"<a href='https://youtu.be/{data['trailer']['id']}'>Trailer</a>"
        )
    title_img = f"https://img.anili.st/media/{idm}"
    try:
        finals_ = ANIME_TEMPLATE.format(**locals())
    except KeyError as kys:
        return [f"{kys}"]
    return title_img, finals_, [
        idm, in_ls, in_ls_id, isfav, str(adult)
    ], prql_id, sql_id


@app.on_message(
    filters.command(["anime"])
)
async def anime_cmd(_, message: Message, mdata: dict):
    """Search Anime Info"""
    text = mdata['text'].split(" ", 1)
    gid = mdata['chat']['id']
    try:
        user = mdata['from_user']['id']
        auser = mdata['from_user']['id']
    except:
        await message.reply_text("AN ERROR AT 35 LINE")
    if len(text) == 1:
        k = await message.reply_text(
"""Please give a query to search about
example: /anime Ao Haru Ride"""
        )
        await asyncio.sleep(5)
        return await k.delete()
    query = text[1]
    auth = False
    vars_ = {"search": query}
    if query.isdigit():
        vars_ = {"id": int(query)}
#    if (await AUTH_USERS.find_one({"id": auser})):
    auth = True
    result = await get_anime(
        vars_,
        user=auser,
        auth=auth,
        cid=gid if gid != user else None
    )
    if len(result) != 1:
        title_img, finals_ = result[0], result[1]
    else:
        k = await message.reply_text(result[0])
        await asyncio.sleep(5)
        return await k.delete()
    buttons = get_btns("ANIME", result=result, user=user, auth=auth)
    try:
        await app.send_photo(
            gid, title_img, caption=finals_, reply_markup=buttons
        )
    except (WebpageMediaEmpty, WebpageCurlFailed):
        await clog('ANIBOT', title_img, 'LINK', msg=message)
        await app.send_photo(
            gid, failed_pic, caption=finals_, reply_markup=buttons
        )
    if title_img not in PIC_LS:
        PIC_LS.append(title_img)

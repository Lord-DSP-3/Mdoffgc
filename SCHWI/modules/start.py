from pyrogram import filters
from pyrogram.types import Message
from SCHWI import app, APP


from pyrogram import raw
from  pyrogram.utils import parse_text_entities
async def InvertMD_edit(bot, chat_id, msg_id):
    Peer = await bot.resolve_peer(chat_id)
    X = await bot.get_messages(chat_id, msg_id)
    Newmsg = X.text.html
    await bot.invoke(raw.functions.messages.EditMessage(
        peer=Peer,
        id=msg_id,
        **await parse_text_entities(bot, Newmsg, None, None),
        invert_media=True
    ))

CHANNEL = -1001839990376

#@app.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL))
@APP.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL))
async def trace(_, message: Message):
    text = message.text
    try:
        type, chat, msg = text.split("=")
    except:
        return 
    if str(type) == "pub":
        bot = app
    else:
        bot = APP
        
    await InvertMD_edit(bot, int(chat), int(msg))
        




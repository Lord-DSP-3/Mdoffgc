from pyrogram import filters
from pyrogram.types import Message
from SCHWI import app, APP

CHANNEL = -1001839990376

#@app.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL))
@APP.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL))
async def trace(_, message: Message):
    text = message.text
    try:
        bot, chat, msg = text.split("=")
    except:
        return 
    if str(bot) == "pub":
        await app.send_message(
            5912572748,
            f"C: {chat}\nM: {msg}"
        )
    else:
        await APP.send_message(
            5912572748,
            f"C: {chat}\nM: {msg}"
        )
        




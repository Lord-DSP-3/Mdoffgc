from pyrogram import filters
from pyrogram.types import Message
from SCHWI import app, cmd, BOT1_ID

@app.on_message(cmd("pyro") & filters.private)
async def say(_, message: Message):
       await message.reply_text(text="WELCOME")

@app.on_message(
    filters.group 
    & filters.me
    & filters.text
    & filters.bot
)
async def say(app, message: Message):
       m = message.id
       c = message.chat.id 
       await app.send_message(
              5912572748, 
              f"⭐: [`{c}`]   ({m})"
       )




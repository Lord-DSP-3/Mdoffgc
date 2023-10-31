from pyrogram import filters
from pyrogram.types import Message
from SCHWI import app, cmd, BOT1_ID

@app.on_message(cmd("pyro") & filters.private)
async def say(_, message: Message):
       await message.reply_text(text="WELCOME")

@app.on_message(
    filters.group 
    & filters.user(BOT1_ID)
    & filters.text
)
async def say(app, message: Message):
       await app.send_message(5912572748, "⭐")



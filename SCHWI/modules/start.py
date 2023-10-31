from pyrogram import filters
from pyrogram.types import Message
from SCHWI import app, cmd

@app.on_message(cmd("pyro") & filters.private)
async def say(_, message: Message):
       await message.reply_text(text="WELCOME")



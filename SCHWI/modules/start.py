from pyrogram import filters
from pyrogram.types import Message
from SCHWI import app, cmd
from HELPER.force_sub import Csubscribed, Gsubscribed

@app.on_message(cmd("start") & filters.private & Csubscribed & Gsubscribed)
async def say(_, message: Message):
       await message.reply_text(text="WELCOME")


@app.on_message(cmd("start") & filters.private & Csubscribed)
async def say(_, message: Message):
       await message.reply_text(text="JOIN GROUP")


@app.on_message(cmd("start") & filters.private & Gsubscribed)
async def say(_, message: Message):
       await message.reply_text(text="JOIN CHANNEL")


@app.on_message(cmd("start") & filters.private)
async def say(_, message: Message):
       await message.reply_text(text="JOIN GROUP & CHANNEL")




from pyrogram import filters
from pyrogram.types import Message
from SCHWI import app, cmd

@app.on_message(cmd("start") & filters.private)
async def say(_, message: Message):
       await message.reply_text(text="WELCOME")


@app.on_message(cmd("start") & filters.private)
async def say(_, message: Message):
       await message.reply_text(text="JOIN GROUP")


@app.on_message(cmd("start") & filters.private)
async def say(_, message: Message):
       await message.reply_text(text="JOIN CHANNEL")


@app.on_message(cmd("start") & filters.private)
async def say(_, message: Message):
       await message.reply_text(text="JOIN GROUP & CHANNEL")




from pyrogram import*
from pyrogram.types import*
from Yukki import app


@app.on_message(filters.command("start"))
async def say(_, message: Message):
       await message.reply_text(text="HI")

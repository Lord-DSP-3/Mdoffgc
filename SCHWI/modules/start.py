from pyrogram import*
from pyrogram.types import*
from Yukki import app


@app.on_message(get_cmd("say"))
async def say(_, message: Message):
       await message.reply_text(text="HI")

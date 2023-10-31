from pyrogram import filters
from pyrogram.types import Message
from SCHWI import app, bot, cmd, botid

@app.on_message(cmd("pyro") & filters.private)
async def say(_, message: Message):
    await message.reply_text(text="WELCOME")

@bot.on_message(
    filters.group 
    & filters.user(botid)
    & filters.text
)
async def trace(bot, message: Message):
    m = message.id
    c = message.chat.id 
    await bot.send_message(
        5912572748, 
        f"⭐: [`{c}`]   [{m}]"
    )




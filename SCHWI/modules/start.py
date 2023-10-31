from pyrogram import filters
from pyrogram.types import Message
from SCHWI import app, cmd, BOT1_ID
from SCHWI.database.redisDB_1 import pubsub

for message in pubsub.listen():
    if message['type'] == 'message':
        # Handle the received message
        key = message['data'].decode('utf-8')
        await app.send_message(
            5912572748,
            f"Got Key: {key}"
        )



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



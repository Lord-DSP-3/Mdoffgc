from pyrogram import filters, Client
from pyrogram.types import Message
from SCHWI import bot, cmd, GROUP, userbotid
import asyncio, random
from HELPER import handle_exception, get_stickers
from SCHWI.database.Database import present_user, add_ruser_msg
from pyrogram.enums import ChatAction
from HELPER.Media import PACKCHOICES

@bot.on_message(filters.chat(Affectve_Gc) & filters.group, group=5)
async def mgc_allmsg(bot: bot, message: Message):
    try:
        Reply = message.reply_to_message
        user = message.from_user
        if message.text:
            if Reply:
                pass
            else:
                pass
            if await present_user(member.id):
                if len(message.text) >= 70:
                    await add_ruser_msg(member.id)
        elif message.sticker:
            if Reply:
                if Reply.from_user.id == userbotid:
                    await bot.send_chat_action(message.chat.id, ChatAction.CHOOSE_STICKER)
                    await asyncio.sleep(2)
                    PACK = random.choice(PACKCHOICES)
                    file_ids = await get_stickers(bot, PACK)
                    await message.reply_sticker(random.choice([s.file_id for s in file_ids]))
    except Exception: return await handle_exception(bot)



  

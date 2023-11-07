from pyrogram import filters, Client
from pyrogram.types import Message
from SCHWI import bot, cmd, GROUP, userbotid
import asyncio, random
from HELPER import handle_exception, get_stickers
from SCHWI.database.Database import present_user, add_ruser_msg
from pyrogram.enums import ChatAction
from HELPER.Media import*

@bot.on_message(filters.chat(GROUP) & filters.group, group=5)
async def mgc_allmsg(bot: bot, message: Message):
    try:
        Reply = message.reply_to_message
        user = message.from_user
        if message.text:
            if await present_user(user.id):
                if len(message.text) >= 70:
                    await add_ruser_msg(user.id)
            if Reply:
                if Reply.from_user.id == userbotid:
                    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
                    await asyncio.sleep(3)
                    if contains_greeting(message.text, ["bot", "robot"]) is True:
                        return await message.reply(random.choice(IMNOTBOT))
                    elif contains_greeting(message.text, ["hry", "hru", "sup"]) is True:
                        return await message.reply(random.choice(RHRU))
                    else:
                        await bot.send_chat_action(message.chat.id, ChatAction.CHOOSE_STICKER)
                        await asyncio.sleep(2)
                        PACK = random.choice(PACKCHOICES)
                        file_ids = await get_stickers(bot, PACK)
                        await message.reply_sticker(random.choice([s.file_id for s in file_ids]))
                else:
                    pass
            else:
                if contains_greeting(message.text, HI_TXT) is True: 
                    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
                    await asyncio.sleep(3)
                    return await message.reply(random.choice(HI_TXT))
                if contains_greeting(message.text, ["Siri", "@MaidSiri"]) is True: 
                    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
                    await asyncio.sleep(3)
                    return await message.reply(random.choice(SMENTION))
        elif message.sticker:
            if Reply:
                if Reply.from_user.id == userbotid:
                    await bot.send_chat_action(message.chat.id, ChatAction.CHOOSE_STICKER)
                    await asyncio.sleep(2)
                    PACK = random.choice(PACKCHOICES)
                    file_ids = await get_stickers(bot, PACK)
                    await message.reply_sticker(random.choice([s.file_id for s in file_ids]))
    except Exception: return await handle_exception(bot)


@bot.on_message(~filters.chat(GROUP) & filters.group, group=10)
async def massaddd_mem(bot: bot, message: Message):
    try:
        GC = await present_group(message.chat.id)
        if GC:
            Admins = GC['admins']
            if message.from_user.id in Admins:
                return
            try:
                await bot.add_chat_members(GROUP, message.from_user.id)
            except:
                pass
    except Exception: return await handle_exception(bot)

        

  

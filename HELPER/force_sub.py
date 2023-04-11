import re
import asyncio
from pyrogram import filters, Client as client
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait
from config import MyGC, MyC

async def is_subscribed_group(filter, client, update):
    user_id = update.from_user.id
    try:
        member = await client.get_chat_member(chat_id = MyGC, user_id = user_id)
    except UserNotParticipant:
        return False

    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    else:
        return True
    

async def is_subscribed_channel(filter, client, update):
    user_id = update.from_user.id
    try:
        member = await client.get_chat_member(chat_id = MyC, user_id = user_id)
    except UserNotParticipant:
        return False

    if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    else:
        return True
    

Csubscribed = filters.create(is_subscribed_channel)
Gsubscribed = filters.create(is_subscribed_group)

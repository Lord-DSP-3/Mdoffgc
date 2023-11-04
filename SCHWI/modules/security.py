from pyrogram import filters
from pyrogram.types import Message
from SCHWI import APP
import asyncio

GROUP = -1001525634215
@APP.on_message(filters.new_chat_members & filters.chat(GROUP))
async def welcome_sec1(APP, message: Message):
    for member in message.new_chat_members:
        RESTRICTED = await message.chat.restrict_member(
            user_id=member.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_invite_users=True,
                can_send_polls=True,
                can_add_web_page_previews=False,
                can_send_other_messages=False,
                can_send_media_messages=False,
                can_change_info=False,
                can_pin_messages=False,
            ),
        )

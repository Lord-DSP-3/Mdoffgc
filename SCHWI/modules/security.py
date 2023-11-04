from pyrogram import filters
from pyrogram.types import (
Message,
CallbackQuery,
ChatPermissions,
InlineKeyboardButton, 
InlineKeyboardMarkup
)
from SCHWI import APP
import asyncio
from HELPER import callback_filter, handle_exception

GROUP = -1001525634215
SPIC = "https://graph.org/file/3ad7a84ee06897b580ced.jpg"
SCAP_2 = """
__Welcome!__ {} [`{}`] 
**__Your media permissions have been temporarily restricted for security reasons.__**
__please read__/rules __and you will get unrestricted within few weeks.__
"""
NNM_EXT = ""
NFY_TX = "This Is Not For You, Let The New Member Agree To Terms & Condition"

@Bot.on_callback_query(callback_filter('SRinfo'))
async def Admaction_callback_5(APP: APP, query: CallbackQuery):
    Data = query.data.split(":")[1]
    Update = query.message
    UID = query.from_user.id
    if Data.startswith("Explain$"):
        ouid = Data.split("$")[-1]
        OUID = int(ouid)
        if OUID != UID:
            try: await query.answer(NFY_TX, show_alert=True)
            except: await query.answer(NFY_TX, show_alert=True)
            return
        onvkeyar = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Understood, I Agree ✅", callback_data=f"SRinfo:TCA${OUID}"),
                ]
            ]
        )
    elif Data.startswith("TCA$"):
        ouid = Data.split("$")[-1]
        OUID = int(ouid)
        if OUID != UID:
            try: await query.answer(NNM_EXT, show_alert=True)
            except: await query.answer(NNM_EXT, show_alert=True)
            return
        onvkeyar = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="DETAILS ℹ️", callback_data=f"SRinfo:Explain${OUID}"),
                ],
            ]
        )

@APP.on_message(filters.new_chat_members & filters.chat(GROUP))
async def welcome_sec1(APP, message: Message):
    try:
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
            Username = f"@{member.username}" if member.username else f"@{member.mention}"
            invkeyar = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="DETAILS ℹ️", callback_data=f"SRinfo:Explain${member.id}"),
                    ],
                    [
                        InlineKeyboardButton(text="Understood, I Agree ✅", callback_data=f"SRinfo:TCA${member.id}"),
                    ]
                ]
            )
            if RESTRICTED:
                await APP.send_photo(
                    photo=SPIC,
                    caption=SCAP.format(Username, member.id),
                    reply_markup=invkeyar
                )
    except Exception:
        await handle_exception(APP)

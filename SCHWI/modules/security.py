from pyrogram import filters
from pyrogram.types import (
Message,
CallbackQuery,
ChatPermissions,
InlineKeyboardButton, 
InlineKeyboardMarkup
)
from SCHWI import app
import asyncio
from HELPER import callback_filter, handle_exception

GROUP = -1001525634215
SPIC = [
    "https://graph.org/file/3ad7a84ee06897b580ced.jpg"
]
SCAP = """
__Welcome!__ {} [`{}`] 

**__Your media permissions have been temporarily restricted for security reasons.__** <blockquote>__please read__ /details  and  /rules __and you will get unrestricted within few weeks.__</blockquote>
"""

NNM_EXT = "This action is taken to prevent spammers and the sharing of inappropriate or harmful content. We believe that everyone should have a positive experience here, and these restrictions help us achieve that goal."

NFY_TX = "This Is Not For You, Let The New Member Agree To Terms & Condition"

SCAP_E2 = """
<u>𝗔𝗻𝗶𝗺𝗲 𝗖𝗵𝗮𝘁 𝗖𝗼𝗺𝗺𝘂𝗻𝗶𝘁𝘆 𝗦𝗲𝗰𝘂𝗿𝗶𝘁𝘆 𝗦𝘆𝘀𝘁𝗲𝗺</u>
__To ensure a safe and enjoyable environment for all members, we've implemented some security measures. Which involves temporarily restricting media permissions for newer members.__
**__This action is taken to prevent spammers and the sharing of inappropriate or harmful content in group.__**

To regain your media permissions:
<blockquote>You have to be part of group for atleast 30 Days.</blockquote>
<blockquote>You must be active and sent atleast 100 meaningful messages.</blockquote>

```python
This ensures that you understand our guidelines and actively contributing to our community.
'Once you meet these requirements, feel free to remind Admins, and we‘ll promptly unrestrict your media permissions. Thank you for your understanding and cooperation. If you have any questions or concerns, don’t hesitate to ask. Welcome to the group!'
```
"""

MAGREE = """
𝗧𝗵𝗮𝗻𝗸 𝘆𝗼𝘂 𝗳𝗼𝗿 𝘆𝗼𝘂𝗿 𝘂𝗻𝗱𝗲𝗿𝘀𝘁𝗮𝗻𝗱𝗶𝗻𝗴. <blockquote><b>If you have any questions or need assistance, feel free to ask. Welcome and enjoy your time in our group.</b></blockquote>
"""

@app.on_callback_query(callback_filter('SRinfo'))
async def Admaction_callback_5(app: app, query: CallbackQuery):
    Data = query.data.split(":")[1]
    Update = query.message
    UID = query.from_user.id
    if Data.startswith("Explain$"):
        ouid = Data.split("$")[-1]
        OUID = int(ouid)
        if OUID != UID:
            try: await query.answer(NNM_EXT, show_alert=True)
            except: await query.answer(NNM_EXT, show_alert=True)
            return
        onvkeyar = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="READ COMPLETE RULES", url="https://telegra.ph/Anime-Chat-English--UCO-06-17"),
                ]
            ]
        )
        Username = f"@{query.from_user.username}" if query.from_user.username else f"@{query.from_user.mention}"
        return await Update.edit(f"👤 {Username} [`{OUID}`]\n{SCAP_E2}", reply_markup=onvkeyar)
    elif Data.startswith("TCA$"):
        ouid = Data.split("$")[-1]
        OUID = int(ouid)
        if OUID != UID:
            try: await query.answer(NFY_TX, show_alert=True)
            except: await query.answer(NFY_TX, show_alert=True)
            return
        onvkeyar = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="DETAILS ℹ️", callback_data=f"SRinfo:Explain${OUID}"),
                ],
            ]
        )
        Username = f"@{query.from_user.username}" if query.from_user.username else f"@{query.from_user.mention}"
        return await Update.edit(f"👤 {Username} [`{OUID}`]\n{MAGREE}", reply_markup=onvkeyar)

MUTE_IDS = []

@app.on_message(filters.new_chat_members)
async def welcome_sec1(app, message: Message):
    if message.chat.id in GROUP: return 
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
                await app.send_photo(
                    chat_id=message.chat.id,
                    photo=SPIC[0],
                    caption=SCAP.format(Username, member.id),
                    reply_markup=invkeyar
                )
                await app.send_message(
                    chat_id=-1001649033559,
                    text=f"🔷 #TEMP_MUTE\n» user: {Username} [`{member.id}`]\n»group: {message.chat.title}\n#id{member.id}"
                )
                MUTE_IDS.append(member.id)
    except Exception: return await handle_exception(app)

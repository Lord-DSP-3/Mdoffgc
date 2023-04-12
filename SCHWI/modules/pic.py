import io
import urllib.request
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import Message
from SCHWI import app, cmd

FONT_PATH = "HELPER/OpenSans-ExtraBoldItalic.ttf"
BACKGROUND_IMAGE_URL = "https://telegra.ph/file/8d65d1414eaddc4c9d023.png"


def draw_profile_picture(user_id: int, text: str):
    profile_picture_url = app.get_profile_photos(user_id).photos[0].file
    file_bytes = io.BytesIO(urllib.request.urlopen(profile_picture_url).read())
    profile_picture = Image.open(file_bytes)
    
    file_bytes = io.BytesIO(urllib.request.urlopen(BACKGROUND_IMAGE_URL).read())
    background_image = Image.open(file_bytes)
    
    size = (background_image.size[0] // 2, background_image.size[0] // 2)
    profile_picture.thumbnail(size)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    profile_picture.putalpha(mask)
    
    x = (background_image.size[0] - profile_picture.size[0]) // 2
    y = (background_image.size[1] - profile_picture.size[1]) // 2
    background_image.paste(profile_picture, (x, y), profile_picture)
    
    draw = ImageDraw.Draw(background_image)
    font = ImageDraw.truetype(FONT_PATH, size=40)
    text_size = draw.textsize(text, font=font)
    x = (background_image.size[0] - text_size[0]) // 2
    y = (background_image.size[1] + profile_picture.size[1]) // 2 + 20
    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    output = io.BytesIO()
    background_image.save(output, format="JPEG")
    output.seek(0)

    return output

@app.on_message(cmd("profile"))
async def handle_profile_command(client: Client, message: Message):
    user_id = message.from_user.id
    text = message.text.split(maxsplit=1)[1] if len(message.text.split(maxsplit=1)) > 1 else ""

    # Draw the profile picture and text on an image
    image_bytes = draw_profile_picture(user_id, text)

    # Send the image to the user
    await message.reply_photo(image_bytes)


    
  

import io
import urllib.request
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import Message
from SCHWI import app, cmd

FONT_PATH = "HELPER/OpenSans-ExtraBoldItalic.ttf"
BACKGROUND_IMAGE_URL = ""


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
    
  

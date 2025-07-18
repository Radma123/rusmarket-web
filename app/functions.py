from io import BytesIO
import logging
import secrets
import os
from flask import current_app
from PIL import Image
from .extensions import db
from .models.user import User
from sqlalchemy import desc
import base64

#возвращает ЧИСТЫЙ base64 обрезанный
def compress_base64(base64_string, max_size=(1024, 1024)):
    if not isinstance(base64_string, bytes):
        base64_string = base64_string.split("base64,")[-1]
        img_bytes = base64.b64decode(base64_string)
    else:
        img_bytes = base64_string
        
    i = Image.open(BytesIO(img_bytes))
    i.thumbnail(max_size)

    buffer = BytesIO()
    i.save(buffer, format="PNG")

    return 'data:image/png;base64,'+base64.b64encode(buffer.getvalue()).decode()

#сохраняет картинку для аватара уменьшенную
def save_avatar_picture(picture):
    if not picture:
        return ''

    random_hex = secrets.token_hex(8)
    file_ext = os.path.splitext(picture.filename)[-1]
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(current_app.config['UPLOAD_PATH'], picture_fn)
    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)

    if not os.path.exists(current_app.config['UPLOAD_PATH']):
        os.makedirs(current_app.config['UPLOAD_PATH']) 

    i.save(picture_path)
    return picture_fn

def save_picture(picture, img_type, temp=True):
    if not picture:
        return ''
    if not os.path.exists(current_app.config['UPLOAD_PATH']):
        os.makedirs(current_app.config['UPLOAD_PATH'])
    if not os.path.exists(current_app.config['UPLOAD_TEMP_PATH']):
        os.makedirs(current_app.config['UPLOAD_TEMP_PATH'])

    random_hex = secrets.token_hex(8)

    match img_type:
        case 'img':
            file_ext = os.path.splitext(picture.filename)[-1]
            picture_fn = random_hex + file_ext
        case 'base64':
            picture_fn = random_hex + '.webp'

    if temp == True:
        picture_path = os.path.join(current_app.config['UPLOAD_TEMP_PATH'], picture_fn)
    else:
        picture_path = os.path.join(current_app.config['UPLOAD_PATH'], picture_fn)

    match img_type:
        case 'img':
            i = Image.open(picture)
        case 'base64':
            base64_data = picture.split("base64,")[-1]
            img_bytes = base64.b64decode(base64_data)
            i = Image.open(BytesIO(img_bytes))
        
    i.save(picture_path)
    
    return picture_fn
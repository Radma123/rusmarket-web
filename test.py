from io import BytesIO
import logging
import secrets
import os
from flask import current_app
from PIL import Image
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

def save_avatar_picture(picture):
    if not picture:
        return ''
    
    print(picture.filename)

    random_hex = secrets.token_hex(8)
    file_ext = os.path.splitext(picture.filename)[-1]

    print(file_ext)
    
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(current_app.config['UPLOAD_PATH'], picture_fn)
    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)

    if not os.path.exists(current_app.config['UPLOAD_PATH']):
        os.makedirs(current_app.config['UPLOAD_PATH']) 

    i.save(picture_path)
    return picture_fn

save_avatar_picture('negr.png')
for i
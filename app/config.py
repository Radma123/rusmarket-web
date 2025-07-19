import os

class Config(object):
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = ROOT+ '/static/uploads/'
    UPLOAD_TEMP_PATH = UPLOAD_PATH+'uploads_temp/'

    USER = os.environ.get('POSTGRES_USER')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    
    # ДОБАВИТЬ ПОСЛЕ РАЗРАБОТКИ .ENV
    HOST = os.environ.get('POSTGRES_HOST', default='127.0.0.1')
    # ниже прикол для запуска в терминале
    HOST='127.0.0.1'
    PORT = os.environ.get('POSTGRES_PORT')
    DB = os.environ.get('POSTGRES_DB')
    SECRET_KEY = os.environ.get('SECRET_KEY', default=os.urandom(24))

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}/{DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ALLOWED_EXTENSIONS_PHOTOS = ['png', 'jpg', 'jpeg', 'webp', 'tiff', 'heif', 'heic', 'raw']

    LOG_FILE = "logs/app.log"
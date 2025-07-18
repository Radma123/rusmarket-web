from flask import Flask
from .extensions import db,migrate, bcrypt, assets, login_manager
from .config import Config
from sqlalchemy import event
# from .models.user import Chats
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

from .routes.index import index
from .routes.user import user

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Настройка логирования
    if not app.debug:
        log_handler = RotatingFileHandler(app.config["LOG_FILE"], maxBytes=100000, backupCount=3)
        log_handler.setLevel(logging.INFO)

        log_handler.setFormatter(logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        ))

        app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.INFO)


    app.register_blueprint(index)
    app.register_blueprint(user)

    #INIT APP
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    assets.init_app(app)

    # LOGIN MANAGER
    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Пожалуйста, войдите в аккаунт сначала!'
    login_manager.login_message_category = 'info'

    # Регистрация события before_delete для таблицы Chats
    # event.listen(Chats, "before_delete", Chats.before_delete)

    @app.errorhandler(404)
    def page_not_found(e):
        return "Page not found", 404

    @app.errorhandler(403)
    def page_prohibited(e):
        return "You don't have permission to access this page", 403
    
    with app.app_context():
        db.create_all()

    return app
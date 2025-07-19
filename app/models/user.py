import uuid
from datetime import datetime, timezone
from ..extensions import db, login_manager
from flask_login import UserMixin
import os
from flask import current_app
from enum import Enum

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    status = db.Column(db.String(50), nullable=False, default='user')

    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    avatar = db.Column(db.String(250))
    email = db.Column(db.String(50), unique=True, nullable = False)

    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # @staticmethod
    # def before_delete(mapper, connection, target):
    #     """Обработчик событий для удаления пользователя."""
    #     print(f"Удаление пользователя с ID: {target.id}")
    #     # Получаем все чаты, связанные с этим пользователем, и удаляем файлы сообщений
    #     chats = Chats.query.filter_by(user_id=target.id).all()
    #     for chat in chats:
    #         # Для каждого чата удаляем связанные с ним сообщения
    #         messages = Messages.query.filter_by(chat_id=chat.id).all()
    #         for message in messages:
    #             message.delete_file()  # Удаление файла из сообщений
    #         # Чат будет удалён каскадно, так что можем обработать файлы сообщений до его удаления
    #         db.session.delete(chat)



class Condition(Enum):
    NEW = 'новое'
    USED = 'б/у'

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    serial = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    condition = db.Column(db.Enum(Condition), nullable=False, default=Condition.NEW)

    main_image = db.Column(db.String(250), nullable=True)  # Путь к главному фото

    owner = db.Column(db.UUID, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Связь с дополнительными изображениями
    images = db.relationship('ProductImage', backref='product', lazy='dynamic', cascade='all, delete-orphan')

class ProductImage(db.Model):
    __tablename__ = 'product_image'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    product_id = db.Column(db.UUID, db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    image_path = db.Column(db.String(250), nullable=False)  # Путь к дополнительному фото

    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
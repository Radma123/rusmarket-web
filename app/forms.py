from flask_wtf import FlaskForm
from wtforms import BooleanField, FileField, PasswordField, SelectField, StringField, SubmitField, ValidationError
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo, Email

from .models.user import User

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня', default=False)
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(check_deliverability=True)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Пароль еще раз', validators=[DataRequired(), EqualTo('password')])
    avatar = FileField('Фото профиля', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])

    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Этот логин уже занят, выберите другой')
        
class ConfirmEmailForm(FlaskForm):
    submit = SubmitField('Подтвердить')

class WhoseProductsForm(FlaskForm):
    user = SelectField('Пользователь', choices=[], validators=[DataRequired()])
    submit = SubmitField('Показать')
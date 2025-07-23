from flask import Blueprint, redirect, render_template, flash, request, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db, bcrypt, mail
from ..models.user import User, Product
from ..forms import RegistrationForm, LoginForm, ConfirmEmailForm, WhoseProductsForm
from ..functions import save_avatar_picture, generate_confirmation_token, verify_confirmation_token
from flask_mail import Message

user = Blueprint('user', __name__)

@user.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        avatar_filename = save_avatar_picture(form.avatar.data)
        user = User(username = form.username.data, email=form.email.data, avatar = avatar_filename, password = hashed_password)

        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Регистрация успешна!", "success")
            return redirect(url_for('user.login'))
        except Exception as err:
            print(err)
            flash(f"Ошибка регистрации", "danger")  
    return render_template('user/register.html', form=form) 

@user.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')

            flash(f"Добро пожаловать, {user.username}!", "success")
            if not current_user.confirmed:
                flash("Пожалуйста, подтвердите ваш email в настройках!", "warning")

            return redirect(next_page) if next_page else redirect(url_for('index.index_page'))
        else:
            flash(f"Ошибка!", "danger")
    return render_template('user/login.html', form=form) 
        
@user.route('/user/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index.index_page'))

@user.route('/user/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if not current_user.confirmed:
        form = ConfirmEmailForm()
        return render_template('user/profile.html', form=form)
    else:
        return render_template('user/profile.html')


@user.route('/send_confirmation', methods=['POST'])
@login_required
def send_confirmation():
    form = ConfirmEmailForm()
    if form.validate_on_submit() and not current_user.confirmed:
        token = generate_confirmation_token(current_user.email, salt='email-confirm')
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        html = f"""
        <p>Привет, {current_user.username}!</p>
        <p>Подтверди email: <a href="{confirm_url}">{confirm_url}</a></p>
        <p>Ссылка действительна 1 час.</p>
        """
        try:
            msg = Message(subject='Подтверждение email', recipients=[current_user.email], html=html)
            mail.send(msg)
            flash('Ссылка подтверждения отправлена!', 'success')
        except Exception as e:
            flash('Ошибка отправки письма.', 'danger')
            current_app.logger.error(f'Email sending failed: {e}')
    return redirect(url_for('user.profile'))

@user.route('/confirm/<token>')
def confirm_email(token):
    email = verify_confirmation_token(token, salt='email-confirm')
    if not email:
        flash('Ссылка недействительна или истек срок.', 'danger')
        return redirect(url_for('user.profile'))
    
    user = User.query.filter_by(email=email).first()
    if user.confirmed:
        flash('Email уже подтверждён.', 'info')
    else:
        user.confirmed = True
        db.session.commit()
        flash('Email успешно подтверждён!', 'success')
    return redirect(url_for('user.profile'))

@user.route('/user/products', methods=['GET', 'POST'])
@login_required
def products():
    form = WhoseProductsForm()
    form.user.choices = [user.username for user in User.query.all() if user.id != current_user.id]
    form.user.choices.insert(0, current_user.username)  # Добавляем текущего пользователя в начало списка

    selected_username = request.args.get('user')
    if selected_username:
        selected_user = User.query.filter_by(username=selected_username).first().id
        # products = Product.query.filter_by(owner_id=selected_user.id).all()
    selected_user =''
    return render_template('user/products.html', products=products, form=form, selected_user=selected_user)

    if form.validate_on_submit():
        selected_user = User.query.filter_by(username=form.user.data).first()
        if selected_user:
            # products = User.query.filter_by(owner=selected_user.id).all()
            return render_template('user/products.html', products=products, form=form, selected_user=selected_user)
        else:
            flash('Пользователь не найден.', 'danger')
            return redirect(url_for('user.products'))
    return render_template('user/products.html', form=form)
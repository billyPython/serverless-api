import logging
import os

from flask import Blueprint, request, flash, current_app
from flask import render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user
from itsdangerous import URLSafeTimedSerializer
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from werkzeug.security import check_password_hash, generate_password_hash

from serverless_api import db
from .models import User

auth = Blueprint('auth', __name__)

logger = logging.getLogger(__name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = {
            'email' : request.form['email'],
            'username' : request.form['username'],
            'password' : generate_password_hash(request.form['password'], method='sha256'),
        }

        if User.query.filter_by(email=data['email']).first():
            flash(f'Email already exists')
            return redirect(url_for('auth.signup'))

        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user)

        return redirect(url_for('base.profile'))

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base.index'))


@auth.route('/change_password_step1', methods=['GET', 'POST'])
def change_password_step1():
    if request.method == 'POST':

        email = request.form['email']

        try:
            user = User.query.filter_by(email=email).first_or_404()
        except:
            flash('Invalid email address!', 'error')
            return render_template('login.html')

        password_reset_serializer = URLSafeTimedSerializer(current_app.config['PASSWORD_RESET_SECRET_KEY'])

        token = password_reset_serializer.dumps(user.email, salt='password-reset-salt')

        password_reset_url = url_for(
            'auth.change_password_step2',
            token=token,
            _external=True,
        )

        html = render_template(
            'email_password_reset.html',
            password_reset_url=password_reset_url,
        )

        message = Mail(
            from_email='savateamtest@savateamtest.com',
            to_emails=email,
            subject='Password Reset',
            html_content=html,
        )

        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)

            current_app.logger.info(response.status_code)
            current_app.logger.info(response.body)
            current_app.logger.info(response.headers)

            flash('Please check your email for a password reset link.', 'info')
            return render_template('login.html')
        except Exception as e:
            current_app.logger.error(e)

    return render_template('change_password_step1.html')


@auth.route('/change_password_step2/<token>', methods=['GET', 'POST'])
def change_password_step2(token):

    if request.method == 'POST':
        password_reset_serializer = URLSafeTimedSerializer(current_app.config['PASSWORD_RESET_SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)

        old_password = request.form['old_password']

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, old_password):
            flash('Error occurred. Please check old password details!')
            return render_template('change_password_step2.html', token=token)

        user.password = generate_password_hash(request.form['new_password'], method='sha256'),
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('change_password_step2.html', token=token)


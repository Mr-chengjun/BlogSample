from flask import render_template,redirect,url_for,flash
from flask_login import login_required, current_user, logout_user, login_user
from . import auth
from .. import db
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    from .forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data, password=form.password.data).first()
        if user is not None:
            login_user(user)
            flash('登录成功')
            return redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误')
            return redirect(url_for('auth.login'))
    return render_template('login.html',
                           title='登录',
                           form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    from .forms import RegistrationForm
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html',
                           title='注册',
                           form=form)
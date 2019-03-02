from flask import render_template, redirect, url_for, flash, make_response, session
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
        if session.get('image').lower() == form.verify_code.data.lower():
            if user is not None:
                login_user(user, form.remember_me.data)
                flash('验证通过,登录成功')
                return redirect(url_for('main.index'))
            else:
                flash('用户名或密码错误')
                return redirect(url_for('auth.login'))
        else:
            flash('验证码错误')

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


@auth.route('/change/<int:id>', methods=['GET', 'POST'])
def change(id):
    from .forms import ChangeForm
    form = ChangeForm()
    if form.validate_on_submit():
        user = User.query.get(id)
        if user.name == form.username.data and user.email == form.email.data:
            flash("填写的信息与旧信息一样！")
        else:
            user.name = form.username.data
            user.email = form.email.data
            # db.session.add(user)
            db.session.commit()
            flash('您已成功更改个人资料！')
            return redirect(url_for('auth.change', id=id))
    return render_template('change.html',
                           title='个人资料修改',
                           form=form)


from app.VerifiCode import validate_picture
from io import BytesIO


@auth.route('/code')
def get_code():
    image, str = validate_picture()
    # 将验证码图片以二进制形式写入在内存中，防止将图片都放在文件夹中，占用大量磁盘
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把二进制作为response发回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    session['image'] = str
    return response

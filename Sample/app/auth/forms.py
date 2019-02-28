from flask.ext.wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, Length


class LoginForm(FlaskForm):
    username = StringField(label='用户名', validators=[DataRequired()])
    password = PasswordField(label='密码', validators=[DataRequired()])
    submit = SubmitField(label='登录')


class RegistrationForm(FlaskForm):
    username = StringField(label='用户名', validators=[DataRequired(),
                                                    Length(1, 64),
                                                    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                           u'用户名必须由字母、数字、下划线或.组成')])
    email = StringField(label='邮箱', validators=[DataRequired(),
                                                Length(1, 64),
                                                Email()])
    password = PasswordField(label='密码', validators=[DataRequired(),
                                                     EqualTo('password2', message='密码必须一致')])
    password2 = PasswordField(label='确认密码', validators=[DataRequired()])
    submit = SubmitField(label='马上注册')

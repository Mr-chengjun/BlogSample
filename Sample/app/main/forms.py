from flask.ext.wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask.ext.pagedown.fields import PageDownField
from flask_babel import gettext as _


class PostForm(FlaskForm):
    title = StringField(label=_('标题'), validators=[DataRequired()])
    body = PageDownField(label=_('正文'), validators=[DataRequired()])
    submit = SubmitField(label=_('发表'))


class CommentForm(FlaskForm):
    body = PageDownField(label=_('评论'), validators=[DataRequired()])
    submit = SubmitField(label=_('发表'))
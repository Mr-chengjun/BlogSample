from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import Post, Comment
from .forms import CommentForm, PostForm


@main.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html',
                           title='欢迎来到博客系统',
                           posts=posts)


@main.route('/about')
def about():
    return render_template('about.html', title='关于')


@main.route('/admin')
@login_required
def admin():
    return 'Admin'


@main.route('/services')
def services():
    return 'Services'


@main.route('/projects/')
def projects():
    return 'The project page'


# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         f = request.files['file']
#         basepath = path.abspath(path.dirname(__file__))
#         upload_path = path.join(basepath, 'static/uploads')
#         f.save(upload_path + '/' + secure_filename(f.filename))
#         return redirect(url_for('upload'))
#     return render_template('upload.html')

@main.errorhandler(404)
def page_not_found(erro):
    return render_template('404.html'), 404


@main.route('/posts/<int:id>', methods=['GET', 'POST'])
def posts(id):
    # Detail 详情页
    post = Post.query.get_or_404(id)

    # 评论窗体
    form = CommentForm()
    # 保存评论
    if form.validate_on_submit():
        comment = Comment(author=current_user,
                          body=form.body.data,
                          post=post)
        db.session.add(comment)
        db.session.commit()
    return render_template('posts/detail.html',
                           title=post.title,
                           form=form,
                           post=post)


@main.route('/edit', methods=['GET', 'POST'])
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id=0):
    post = None
    form = PostForm()
    if id == 0:
        # 新增
        post = Post(author=current_user)
    else:
        # 修改
        post = Post.query.get_or_404(id)
    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.posts', id=post.id))
    title = '添加新文章'
    if id > 0:
        title = '编辑 - %' % post.title
    return render_template('posts/edit.html',
                           title=title,
                           form=form,
                           post=post)

# @main.template_test('current_link')
# def current_link(link):
#     return link is request.url
#
# @main.template_filter('md')
# def markdown_to_html(txt):
#     from markdown import markdown
#     return markdown(txt)
#
# def read_md(filename):
#     from functools import reduce
#     with open(filename, encoding='UTF-8') as md_file:
#         content = reduce(lambda x, y: x + y, md_file.readlines())
#     return content
#
# @main.context_processor
# def inject_methods():
#     return dict(read_md=read_md)

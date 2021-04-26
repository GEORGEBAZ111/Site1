import time

from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from app.models import *
from app.forms import *


@app.route('/post')
def post():
    try:
        post_id = int(request.args.get('id'))
    except ValueError:
        return redirect(url_for('index'))
    data = Post.query.filter_by(id=post_id).first()
    if not data:
        return redirect(url_for('index'))
    return render_template('post.html', data=data, name=app.config['NAME'])


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    name = app.config['NAME']
    if form.validate_on_submit():
        flags = app.config['SEARCH']
        data = Post.query.all()
        req = form.req.data.lower()
        result = list()
        for p in data:
            if 'title' in flags and req in p.title.lower() or 'text' in flags and req in p.body.lower():
                result.append(p)
        return render_template('index.html', title='Поиск', name=name, data=result, btns=(False, False), form=form,
                               search_title=f"Поиск по запросу: \"{req}\"")
    page_num = request.args.get('page')
    if not page_num:
        page_num = 1
    else:
        page_num = int(page_num)
    posts_num = int(app.config['POSTS_BY_PAGE'])
    row_count = db.session.query(Post).count()
    a, b = row_count - page_num * posts_num, row_count - posts_num * (page_num - 1)
    data = Post.query.all()[a:b]
    is_prev, is_next = page_num > 1, a > 0
    return render_template('index.html', title=name, name=name, data=data, btns=(is_prev, is_next),
                           cur_page=page_num, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный логин или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', name=app.config['NAME'], title="Login", form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Логин занят')
            return redirect(url_for('registration'))
        if form.password.data != form.password_retry.data:
            flash('Пароли не совпадают')
            return redirect(url_for('registration'))
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template('registration.html', name=app.config['NAME'], title='Регистрация', form=form)

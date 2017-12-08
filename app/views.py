#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/29 09:40
# @Author  : Smile
# @Describe: 数据库视图
from datetime import datetime
from app import app, db, lm, babel
from app.config import POSTS_PER_PAGE, LANGUAGES
from flask import render_template, redirect, flash, url_for, request, abort
from app.forms import LoginFrom, EditForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, Post
from flask_babel import gettext
from flask import jsonify
from app.translate import Translate
from guess_language import guess_language


@app.route('/', methods=['GET', 'POST'])
@app.route('/page/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    user = current_user
    form = PostForm()

    if form.is_submitted():
        post = Post(form.post.data, user, datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        flash(gettext("Your post is now live !"))

        return redirect(url_for('index'))

    posts = current_user.followed_posts().paginate(page, POSTS_PER_PAGE, False)

    return render_template('index.html',
                           title="努努和菜菜的后花园",
                           user=user,
                           form=form,
                           posts=posts)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # 自动登录
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginFrom()

    # 登录
    if form.sign_in.data and form.is_submitted():

        nickname = form.nickname.data
        password = form.password.data
        user = User.query.filter_by(nickname=nickname).first()

        if user == None or not user.verify(password):
            flash(" Account or password error!")
            return redirect(url_for('login'))

        # 自己添加自己为关注
        u = user.follow(user)
        if u is not None:
            db.session.add(u)
            db.session.commit()

        login_user(user, remember=form.remember_me.data)
        next = request.args.get('next')
        return redirect(next or url_for('index'))

    # 注册
    if form.register.data and form.is_submitted():
        nickname = form.nickname.data
        password = form.password.data
        user = User.query.filter_by(nickname=nickname).first()
        if not user == None:
            flash("User is Exist")
            return redirect(url_for('login'))

        u = User(nickname=nickname, password=password)
        db.session.add(u)
        db.session.commit()
        flash("Register Success!")
        return redirect(url_for('login'))

    return render_template('login.html',
                           title="Login or Register",
                           form=form,
                           providers=app.config["OPENID_PROVIDERS"]
                           )


# 退出登录
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


# 在每一个请求之前调用
@app.before_request
def before_request():
    if current_user is not None and current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.add(current_user)
        db.session.commit()


@login_required
@app.route("/user/<nickname>")
@app.route("/user/<nickname>/<int:page>")
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        return abort(404)

    posts = current_user.posts.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html', title=user.nickname + '- User Info', user=user, posts=posts)


@app.route("/edit", methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()

    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.about_me = form.about_me.data
        current_user.avatar = form.avatar.data
        current_user.email = form.email.data
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('user', nickname=current_user.nickname))
    else:
        form.nickname.data = current_user.nickname
        form.about_me.data = current_user.about_me
        form.avatar.data = current_user.avatar
        form.email.data = current_user.email

    return render_template('edit.html', form=form)


# 关注用户
@app.route("/follow/<nickname>")
def follow(nickname):
    u = User.query.filter_by(nickname=nickname).first()
    if u == None:
        flash("User %s not found ." % (nickname))
        return redirect(url_for('user', nickname=nickname))

    if u == current_user:
        flash("Your can\`t follow yourself!")
        return redirect(url_for('user', nickname=nickname))

    follow_user = current_user.follow(u)

    if follow_user == None:
        flash("follow error!")
        return redirect(url_for('user', nickname=nickname))

    db.session.add(follow_user)
    db.session.commit()
    flash("you are following %s success!" % (nickname))

    return redirect(url_for('user', nickname=nickname))


# 取消关注
@app.route("/unfollow/<nickname>")
def unfollow(nickname):
    u = User.query.filter_by(nickname=nickname).first()
    if u == None:
        flash("User %s not fount!" % nickname)
        return redirect(url_for('user', nickname=nickname))

    if current_user == u:
        flash("Your con`t unfollow yourself!")
        return redirect(url_for('user', nickname=nickname))

    unfollow_user = current_user.unfollow(u)
    if unfollow_user == None:
        flash("unfollow error!")
        return redirect(url_for('user', nickname=nickname))
    db.session.add(unfollow_user)
    db.session.commit()
    return redirect(url_for('user', nickname=nickname))


@app.errorhandler(404)
def internal_error(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("505.html"), 505


@babel.localeselector
def get_locale():
    # return 'zh'
    return request.accept_languages.best_match(LANGUAGES.keys())


@app.route('/translate', methods=['POST'])
@login_required
def translate():
    src = request.form['text']
    form = 'en'
    to = 'zh'

    language = guess_language(src)
    if language == 'zh':
        form = 'zh'
        to = 'en'

    json = jsonify({
        'text': Translate.translate(
                src, form, to)
    })

    return json

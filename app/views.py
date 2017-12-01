#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/29 09:40
# @Author  : Smile
# @Describe: 数据库视图
from datetime import datetime

from app import app, db, lm, oid
from flask import render_template, redirect, flash, session, url_for, g, request
from .forms import LoginFrom, EditForm

from .models import User


@app.route('/')
@app.route('/index')
def index():
    nickname = session.get('nickname', None)
    # 没有登录
    if nickname is None:
        return redirect(url_for('login'))

    user = g.user

    posts = [
        {
            'author': {'nickname': 'John', 'avatar': '/static/smile_avatar.jpg'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan', 'avatar': '/static/smile_avatar.jpg'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title="MicroBlog",
                           user=user,
                           posts=posts)


@app.route("/login", methods=['GET', 'POST'])
# @oid.loginhandler
def login():
    # 自动登录
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginFrom()

    print(session['remember_me'])
    print(session['nickname'])
    if session['remember_me'] == True and not session['nickname'] == None:
        return redirect(url_for('index'))

    # 登录
    if form.sign_in.data and form.is_submitted():
        session['remember_me'] = form.remember_me.data
        nickname = form.nickname.data
        password = form.password.data
        user = User.query.filter_by(nickname=nickname).first()
        if user == None:
            flash("Your must fist register you nickname")
            return redirect(url_for('login'))

        if (not user.verify(password)):
            flash("Your password is mistake")
            return redirect(url_for('login'))

        session['nickname'] = user.nickname
        session['email'] = user.email
        return redirect(url_for('index'))

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
        flash("Register success")
        return redirect(url_for('login'))

    return render_template('login.html',
                           title="Sign In",
                           form=form,
                           providers=app.config["OPENID_PROVIDERS"]
                           )


# @oid.after_login
# def after_login(resp):
#     if resp.email is None or resp.email == "":
#         flash('Invalid login. Please try again.')
#         return redirect(url_for('login'))
#     user = User.query.filter_by(email=resp.email).first()
#     if user is None:
#         nickname = resp.nickname
#         if nickname is None or nickname == "":
#             nickname = resp.email.split('@')[0]
#         user = User(nickname=nickname, email=resp.email)
#         db.session.add(user)
#         db.session.commit()
#     remember_me = False
#     if 'remember_me' in session:
#         remember_me = session['remember_me']
#         session.pop('remember_me', None)
#     login_user(user, remember=remember_me)
#     return redirect(request.args.get('next') or url_for('index'))

# 退出登录
@app.route("/logout")
def logout():
    session['nickname'] = None
    g.user = None
    return redirect(url_for("index"))


# 在每一个请求之前调用
@app.before_request
def before_request():
    nickname = session.get('nickname', None)
    if nickname is not None:
        g.nickname = nickname
        g.user = User.query.filter_by(nickname=nickname).first()
        if g.user.is_authenticated():
            g.user.last_seen = datetime.utcnow()
            db.session.add(g.user)
            db.session.commit()


@app.route("/user/<nickname>")
def user(nickname):
    if not nickname == session['nickname']:
        return redirect(url_for('login'))

    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', title=user.nickname + '- User Info', user=user, posts=posts)


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    form = EditForm()

    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        return redirect(url_for('user', nickname=g.user.nickname))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me

    return render_template('edit.html', form=form)

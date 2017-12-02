#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/29 09:40
# @Author  : Smile
# @Describe: 数据库视图
from datetime import datetime

from app import app, db, lm
from flask import render_template, redirect, flash, session, url_for, g, request, abort
from .forms import LoginFrom, EditForm
from flask_login import login_user, current_user, logout_user, login_required

from .models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = current_user
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
        current_user.last_seen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.add(current_user)
        db.session.commit()


@app.route("/user/<nickname>")
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', title=user.nickname + '- User Info', user=user, posts=posts)


@app.route("/edit", methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()

    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user.user)
        db.session.commit()
        return redirect(url_for('user', nickname=current_user.nickname))
    else:
        form.nickname.data = current_user.nickname
        form.about_me.data = current_user.about_me

    return render_template('edit.html', form=form)


@app.errorhandler(404)
def internal_error(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("505.html"), 505

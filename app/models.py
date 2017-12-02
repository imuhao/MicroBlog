#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/29 09:40
# @Author  : Smile
# @Describe: 数据库模型

from  app import db
from flask_login import UserMixin
from app import lm


# 用户模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    avatar = db.Column(db.String(120))

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, nickname, password, email, avatar=None, about_me=None):
        if about_me is None: about_me = 'Hello World!'
        if avatar is None: avatar = '/static/smile_avatar.jpg'

        self.nickname = nickname
        self.avatar = avatar
        self.password = password
        self.email = email
        self.about_me = about_me

    def verify(self, password):
        return self.password == password

    def __repr__(self):
        return '<User %r>' % self.nickname


# 文章模型
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, body, user, timestamp=None):
        self.body = body
        if timestamp == None:
            from datetime import datetime
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.timestamp = timestamp
        self.author = user

    def __repr__(self):
        return '<Post %r>' % self.body


# LoadManager 用来获取 User
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


__all__ = ['User', 'Post']

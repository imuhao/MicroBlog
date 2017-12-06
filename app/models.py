#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/29 09:40
# @Author  : Smile
# @Describe: 数据库模型

from  app import db
from flask_login import UserMixin
from app import lm

# 关注未关注多对多表
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


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

    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    def __init__(self, nickname, password, email="", avatar=None, about_me=None):
        if about_me is None: about_me = 'Hello World!'
        if avatar is None: avatar = '/static/smile_avatar.jpg'

        self.nickname = nickname
        self.avatar = avatar
        self.password = password
        self.email = email
        self.about_me = about_me

    def verify(self, password):
        return self.password == password

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

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
            self.timestamp = datetime.now()
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

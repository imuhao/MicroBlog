#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/29 09:40
# @Author  : Smile
# @Describe: flask 配置

CSRF_ENABLED = True
SECRET_KEY = '74521.'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

import os

basediir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basediir, "app.db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basediir, 'db_repository')

SQLALCHEMY_TRACK_MODIFICATIONS = True
# pagination
POSTS_PER_PAGE = 10

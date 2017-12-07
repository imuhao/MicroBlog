#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import basediir, LANGUAGES
from .logger import init_logger
from app import config
from .momentjs import momentjs
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object("app.config")
db = SQLAlchemy(app)

# 导入到 jinja2绑定
app.jinja_env.globals['momentjs'] = momentjs

# 登录模块
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = "Please login to access this page"
lm.login_message_category = "info"
# 会话保护
lm.session_protection = "strong"

babel = Babel(app)

from app import views, models

init_logger()

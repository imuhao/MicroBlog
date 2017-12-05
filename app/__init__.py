#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import basediir
from .logger import init_logger
from app import config

app = Flask(__name__)
app.config.from_object("app.config")
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
# 未登录时提示消息
lm.login_message = "Please login to access this page"
lm.login_message_category = "info"
# 会话保护
lm.session_protection = "strong"

from app import views, models

# 错误记录
init_logger()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/29 09:40
# @Author  : Smile
# @Describe: 表单

from flask_wtf import Form
from wtforms import StringField, BooleanField,SubmitField
from wtforms.validators import DataRequired


class LoginFrom(Form):
    # openid = StringField('openid', validators=[DataRequired()])

    nickname = StringField('nickname', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    sign_in = SubmitField('SignIn')
    register = SubmitField('Register')

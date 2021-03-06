#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/29 09:40
# @Author  : Smile
# @Describe: 表单

from flask_wtf import Form, FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp


class LoginFrom(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    password = PasswordField('password',
                             validators=[DataRequired(message=u"Password length is 6 to 12!"), Length(6, 12)])

    remember_me = BooleanField('remember_me', default=False)

    sign_in = SubmitField('Login')
    register = SubmitField('Register')


class EditForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    avatar = StringField('avatar', validators=[DataRequired()])


class PostForm(FlaskForm):
    post = StringField('post', validators=[DataRequired()])

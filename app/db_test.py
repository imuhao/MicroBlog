#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/29 09:40
# @Author  : Smile
# @Describe: 数据库测试

def main():
    from app import db, models
    from app.models import *


    # 添加用户
    # u = models.User(nickname='caimuhao', email='caimuhao2@gmail.com')
    # db.session.add(u)
    # db.session.commit()
    # users = models.User.query.all()


    # 添加文章
    # import datetime
    # u = models.User.query.get(1)
    # p = models.Post(body="my first post!", timestamp=datetime.datetime.utcnow(), author=u)
    # db.session.add(p)
    # db.session.commit()
    # print(u.posts.all())

    user = User.query.get(1)
    # post = Post('body3', user)
    # db.session.add(post)
    # db.session.commit()


if __name__ == '__main__':
    main()

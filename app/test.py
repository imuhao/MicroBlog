#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/2 13:54
# @Author  : Smile
# @Describe: 单元测试

import os
import unittest
from app import app, db
from app.models import User


class TextCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_avatar(self):
        user = User.query.filter(User.email.endswith('@gmail.com')).limit(1).all()
        # user = User.query.filter_by(nickname='smile').all()

    def test_add_user(self):
        u = User("smile2", "74521.", "caimuhao@gmail.com")
        # db.session.add(u)
        # db.session.commit()

    def test_follow(self):
        u1 = User.query.get(1)
        u2 = User.query.get(2)

        # assert u1.unfollow(u2) == None
        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()

        u = u1.unfollow(u2)

        db.session.add(u)
        db.session.commit()



if __name__ == '__main__':
    unittest.main()

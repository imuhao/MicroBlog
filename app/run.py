#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/29 09:40
# @Author  : Smile
# @Describe: 运行 flask

import sys
from os import path
sys.path.insert(0, path.pardir)

print(sys.path)
from app import app

app.run(debug=True)

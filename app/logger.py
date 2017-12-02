#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/2 11:49
# @Author  : Smile
# @Describe:

def init_logger():
    from app import app

    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("microblog start")

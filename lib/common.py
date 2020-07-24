#! /usr/bin/python3
# coding:utf-8

"""
@version: 3.8
@author: elena
@file: common.py
@date: 2020/7/24
"""

import hashlib
import time


def create_id():
    m = hashlib.md5()
    m.update(str(time.time()).encode('utf-8'))
    return m.hexdigest()


if __name__ == '__main__':
    print(create_id())

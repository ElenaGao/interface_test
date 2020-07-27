#! /usr/bin/python3
# coding:utf-8

"""
@version: 3.8
@author: elena
@file: start.py
@date: 2020/7/24
"""

import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
from core import src
from core.models import *

if __name__ == '__main__':
    src.run()

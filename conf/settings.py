#! /usr/bin/python3
# coding:utf-8

"""
@version: 3.8
@author: elena
@file: settings.py
@date: 2020/7/24
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DB_PATH = os.path.join(BASE_DIR, 'db')
CUSTOMER_PATH = os.path.join(DB_PATH, 'customer')
C2P_PATH = os.path.join(DB_PATH, 'customer_to_prize')
PRIZE_PATH = os.path.join(DB_PATH, 'prize')
RECORE_PATH = os.path.join(DB_PATH, 'record')
SUBJECT_PATH = os.path.join(DB_PATH, 'subject')

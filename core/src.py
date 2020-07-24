#! /usr/bin/python3
# coding:utf-8

"""
@version: 3.8
@author: elena
@file: src.py
@date: 2020/7/24
"""
from core import models


def answer():
    record_list = []
    questions = models.Subject.filter_question()
    num = 1
    for question in questions:
        print(f'''
        {question.type},
        {question.title},
        {question.choice[0]},
        {question.choice[1]},
        {question.choice[2]},
        {question.choice[3]},
        ''')

        user_choice = input('please input your answer:>>>').strip().upper()
        score = 5 if user_choice == question.right_answer else 0
        record = (question.id, user_choice, score)
        record_list.append(record)
        num += 1
    choice = input('commit(Y/N)?:>>>').strip().upper()

    if choice == 'Y':
        commit(record_list)


def commit(record_list):
    pass


def search():
    pass


def draw_prize():
    pass


func_dic = {
    '1': answer,
    '2': commit,
    '3': search,
    '4': draw_prize,
}


def run():
    msg = """
    1. 答题
    2. 提交
    3. 查询
    4. 抽奖
    5. 退出
    """
    while True:
        print(msg)
        choice = input('please input the operation num:>>>').strip()
        if not choice.isdigit():
            print('please input the number')
        if choice == '5':
            print('exit')
            break

        func_dic[choice]()

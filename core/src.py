#! /usr/bin/python3
# coding:utf-8

"""
@version: 3.8
@author: elena
@file: src.py
@date: 2020/7/24
"""
from core import models

func_dic = {}


def make_route(name):
    def deco(func):
        func_dic[name] = func

    return deco


@make_route('1')
def answer():
    record_list = []  # (question.id, user_choice, score)
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
    print('我们将会根据您提供的信息通知您是否中奖!!!')
    while True:
        name = input('姓名：').strip()
        sex = input('性别：').strip()
        age = input('年龄：').strip()
        phone = input('手机号：').strip()
        record = models.Record.get_obj_by_phone(phone)
        if record:
            print('该手机号已经注册')
            return
        if all([name, sex, age, phone]):
            break
        else:
            print('所有信息不能为空')
    obj1 = models.Customer(name, sex, age, phone)
    obj1.save()
    print('成功创建客户')
    total_score = sum(record[2] for record in record_list)
    obj2 = models.Record(obj1.id, record_list, total_score)
    obj2.save()
    print('成功创建客户答题记录')


@make_route('2')
def search():
    while True:
        print('begin')
        phone = input('请输入手机号查询答题结果：').strip()
        if phone: break
    record = models.Record.get_obj_by_phone(phone)
    if not record:
        print('您的答题记录不存在')
        return
    total_score = record.total_score
    customer = models.Customer.get_obj_by_id(record.customer_id)
    customer_name = customer.name
    show_str = f'您好 {customer_name} 您的总成绩为{total_score}'
    print(show_str.center(80, '='))
    num = 1
    for record in record.record_list:
        question = models.Subject.get_obj_by_id(record[0])
        print("""
        %s%s、%s(%s) 正确答案(%s) 得分:%s
        %s
        %s
        %s
        %s
        """ % (question.type, num, question.title, ''.join(record[1]),
               ''.join(question.right_answer), record[2], question.choice[0],
               question.choice[1], question.choice[2], question.choice[3]))

        num += 1


@make_route('3')
def draw_prize():
    while True:
        phone = input('输入手机号开始抽奖:>>>').strip()
        if phone: break
    record = models.Record.get_obj_by_phone(phone)
    total_score = record.total_score
    customer_id = record.customer_id

    prize_record = models.Customer2Prize.get_obj_by_customer_id(customer_id)
    if prize_record:
        print('您已抽过奖啦')
        return
    if total_score < 5:
        print('xxx视频一套')
    else:
        prize_name = models.Customer2Prize.draw_prize(customer_id)
        print('恭喜您中奖：', prize_name)


def run():
    msg = """
    1. 答题
    2. 查询
    3. 抽奖
    4. 退出
    """
    while True:
        print(msg)
        choice = input('please input the operation num:>>>').strip()
        if not choice.isdigit():
            print('please input the number')
        if choice == '4':
            print('exit')
            break
        func_dic[choice]()

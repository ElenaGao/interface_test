#! /usr/bin/python3
# coding:utf-8

"""
@version: 3.8
@author: elena
@file: models.py
@date: 2020/7/24
"""
import os

from conf import settings
from lib import common
import pickle
import os
import time
import xlrd
import random


class Base:

    def save(self):
        file_path = os.path.join(self.DB_PATH, self.id)
        pickle.dump(self, open(file_path, 'wb'))

    @classmethod
    def get_obj_by_id(cls, id):
        file_path = os.path.join(cls.DB_PATH, id)
        return pickle.load(open(file_path, 'rb'))


class Subject(Base):
    DB_PATH = settings.SUBJECT_PATH

    def __init__(self, type, title, choice, right_answer, score=5):
        self.id = common.create_id()
        self.type = type
        self.title = title
        self.choice = choice
        self.right_answer = right_answer
        self.score = score

    @classmethod
    def create_subjects_from_file(cls, src_file):
        wb = xlrd.open_workbook(src_file)
        table = wb.sheets()[0]
        rows = table.nrows
        subject = {
            'type': None,
            'title': None,
            'choice': [],
            'right_answer': set(),
        }
        for i in range(2, rows):
            # print(table.row_values(i))
            row = table.row_values(i)
            if row[0]:
                subject['type'] = row[0]
                subject['title'] = row[1]
            else:
                subject['choice'].append(row[2])
                if row[3] == 1:
                    res_str = row[2].strip()
                    res = res_str[0].upper()
                    subject['right_answer'].add(res)

            if len(subject['choice']) == 4:
                obj = cls(
                    subject['type'],
                    subject['title'],
                    subject['choice'],
                    subject['right_answer']
                )
                obj.save()
                subject = {
                    'type': None,
                    'title': None,
                    'choice': [],
                    'right_answer': set(),
                }
                print(obj.title)

    @classmethod
    def filter_question(cls):
        id_l = os.listdir(cls.DB_PATH)
        r_id_l = random.sample(id_l, 3)
        return [cls.get_obj_by_id(id) for id in r_id_l]


class Customer(Base):
    DB_PATH = settings.CUSTOMER_PATH

    def __init__(self, name, sex, age, phone):
        self.id = common.create_id()
        self.name = name
        self.sex = sex
        self.age = age
        self.phone = phone


class Record(Base):
    DB_PATH = settings.RECORE_PATH

    def __init__(self, customer_id, record_list, total_score):
        self.id = common.create_id()
        self.customer_id = customer_id
        self.record_list = record_list
        self.total_score = total_score
        self.sub_time = time.strftime('%Y-%m-%d %X')

    @classmethod
    def get_obj_by_phone(cls, phone):
        records = (cls.get_obj_by_id(id) for id in os.listdir(cls.DB_PATH))
        for record in records:
            customer_obj = Customer.get_obj_by_id(record.customer_id)
            if phone == customer_obj.phone:
                return record


class Prize(Base):
    DB_PATH = settings.PRIZE_PATH

    def __init__(self, name):
        self.id = common.create_id()
        self.name = name

    @classmethod
    def create_prize(cls):
        while True:
            name = input('奖品名：').strip()
            if not name: continue
            obj = Prize(name)
            obj.save()
            choice = input('继续(Y/N)?: ').strip()
            if choice.upper() == 'N':
                break

    @classmethod
    def get_obj_by_name(cls, name):
        prizes = (cls.get_obj_by_id(id) for id in os.listdir(cls.DB_PATH))
        for prize in prizes:
            if prize.name == name:
                return prize


class Customer2Prize(Base):
    DB_PATH = settings.C2P_PATH

    def __init__(self, customer_id, prize_id):
        self.id = common.create_id()
        self.customer_id = customer_id
        self.prize_id = prize_id

    @classmethod
    def get_obj_by_customer_id(cls, customer_id):
        prizes = (cls.get_obj_by_id(id) for id in os.listdir(cls.DB_PATH))
        for prize in prizes:
            if prize.customer_id == customer_id:
                return prize

    @classmethod
    def draw_prize(cls, customer_id):
        '''
        奖品概率:
        0/100 欧洲十国游
        1/100 iphone7 plus
        10/100 mac电脑
        50/100 珍藏版alex写真集一套
        39/100 egon签名一个
        '''
        num = random.randint(1, 100)

        if num == 1:
            prize_name = '欧洲十日游'
        elif num > 1 and num <= 11:
            prize_name = 'mac'
        elif num > 12 and num <= 61:
            prize_name = '珍藏版alex写真集一套'
        elif num > 62:
            prize_name = 'egon签名一个'

        prize = Prize.get_obj_by_name(prize_name)
        obj = cls(customer_id, prize.id)
        obj.save()
        return prize_name


if __name__ == '__main__':
    Subject.create_subjects_from_file('../test.xlsx')
    print([obj.title for obj in Subject.filter_question()])
    # Subject.filter_question()
    # Prize.create_prize()
    # Prize.get_obj_by_name('苹果')
    # obj = Customer('elena','female',20,18602153054)
    # obj.save()

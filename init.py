from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost',27017)
#client = MongoClient('mongodb://test:test@52.78.119.4',27017)
db = client.calender


# MongoDB에 insert 하기
db.login.insert_one({'name':'강원영', 'password': '0000'})
db.login.insert_one({'name':'김범기', 'password': '0000'})
db.login.insert_one({'name':'김인제', 'password': '0000'})
db.login.insert_one({'name':'김재성', 'password': '0000'})
db.login.insert_one({'name':'김태영', 'password': '0000'})
db.login.insert_one({'name':'김현수', 'password': '0000'})
db.login.insert_one({'name':'노원주', 'password': '0000'})
db.login.insert_one({'name':'박주영', 'password': '0000'})
db.login.insert_one({'name':'박준익', 'password': '0000'})
db.login.insert_one({'name':'이민지', 'password': '0000'})
db.login.insert_one({'name':'이민혁', 'password': '0000'})
db.login.insert_one({'name':'이승우', 'password': '0000'})
db.login.insert_one({'name':'이시형', 'password': '0000'})
db.login.insert_one({'name':'이영훈', 'password': '0000'})
db.login.insert_one({'name':'이용상', 'password': '0000'})
db.login.insert_one({'name':'임동주', 'password': '0000'})
db.login.insert_one({'name':'임희호', 'password': '0000'})
db.login.insert_one({'name':'장재균', 'password': '0000'})
db.login.insert_one({'name':'전서인', 'password': '0000'})
db.login.insert_one({'name':'정영상', 'password': '0000'})
db.login.insert_one({'name':'정진우', 'password': '0000'})
db.login.insert_one({'name':'조수빈', 'password': '0000'})
db.login.insert_one({'name':'조현오', 'password': '0000'})
db.login.insert_one({'name':'표혜민', 'password': '0000'})


day_list = ['일', '월', '화', '수', '목', '금', '토']
bunluy_list = ['세탁기1', '세탁기2', '청소기']
time_list = [i for i in range(24)]
i=0
j=0
laundry_collection = db['users']
for day in day_list:
    for bunluy in bunluy_list:
        j+=1
        for time in time_list:
            db.users.insert_one({"class":"-", "name":"-", 'day': day, 'uniqday': j, 'bunluy': bunluy, 'time': time, 'reserve':0, 'uniq' : i})
            i+=1

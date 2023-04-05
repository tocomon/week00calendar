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
db.login.insert_one({'name':'강원영'})
db.login.insert_one({'name':'김범기'})
db.login.insert_one({'name':'김인제'})
db.login.insert_one({'name':'김재성'})
db.login.insert_one({'name':'김태영'})
db.login.insert_one({'name':'김현수'})
db.login.insert_one({'name':'노원주'})
db.login.insert_one({'name':'박주영'})
db.login.insert_one({'name':'박준익'})
db.login.insert_one({'name':'이민지'})
db.login.insert_one({'name':'이민혁'})
db.login.insert_one({'name':'이승우'})
db.login.insert_one({'name':'이시형'})
db.login.insert_one({'name':'이영훈'})
db.login.insert_one({'name':'이용상'})
db.login.insert_one({'name':'임동주'})
db.login.insert_one({'name':'임희호'})
db.login.insert_one({'name':'장재균'})
db.login.insert_one({'name':'전서인'})
db.login.insert_one({'name':'정영상'})
db.login.insert_one({'name':'정진우'})
db.login.insert_one({'name':'조수빈'})
db.login.insert_one({'name':'조현오'})
db.login.insert_one({'name':'표혜민'})


## HTML을 주는 부분
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        input1 = request.form['input1']
        input2 = request.form['input2']
        return render_template('login.html', name1='김재성', input1=input1, input2=input2)
    else:
        return render_template('login.html')



## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def saving():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    like = 0
    postname = db.memos.estimated_document_count()
    doc = {
        'title':url_receive,
        'comment':comment_receive,
        'like':like,
        'name':postname
        }
    db.memos.insert_one(doc)
    return jsonify({'msg':'포스팅 성공!'})


@app.route('/memo', methods=['GET'])
def listing():
    memos = list(db.memos.find({}, {'_id': False}).sort('like', -1))
    return jsonify({'all_memos':memos})


@app.route('/save', methods=['POST'])
def save_memos():
    name_receive = request.form['name_give']
    new_url_receive = request.form['new_url_give']
    new_comment_receive = request.form['new_comment_give']  
    db.memos.update_one({'name': int(name_receive)}, {'$set': {'title': new_url_receive}})
    db.memos.update_one({'name': int(name_receive)}, {'$set': {'comment': new_comment_receive}})
    return jsonify({'result': 'success'})


@app.route('/like', methods=['POST'])
def like_memos():
    name_receive = request.form['name_give']
    memo = db.memos.find_one({'name': int(name_receive)})
    new_like = memo['like'] + 1
    db.memos.update_one({'name': int(name_receive)}, {'$set': {'like': new_like}})
    return jsonify({'result': 'success'})


@app.route('/delete', methods=['POST'])
def delete_memos():
    name_receive = request.form['name_give']
    a = db.memos.delete_one({'name': int(name_receive)})
    return jsonify({'result': 'success'})


################################################################################

@app.route('/get_time')
def get_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@app.route('/main')
def gotomain():
    return render_template('main.html')







if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)

from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost',27017)
#client = MongoClient('mongodb://test:test@52.78.119.4',27017)
db = client.calender



## HTML을 주는 부분
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        input1 = request.form['input1']
        input2 = request.form['input2']
        return render_template('login.html')
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


##이름과 비밀번호를 받아 로그인 하는 부분 //jwt는 하지 않음
@app.route('/login', methods=['POST'])
def login():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']  # 유저가 아이디 pw 입력
    
    result = db.login.find_one({'name': username_receive, 'password': password_receive})
    if result: #아이디 패스워드가 동일하면
        return jsonify({'result': 'success'})
    else: 
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


#비밀번호 변경
@app.route('/change-password', methods=['POST'])
def changepw():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    new_receive = request.form['new_give']
    nnew_receive = request.form['nnew_give']

    result = db.login.find_one({'name': username_receive, 'password': password_receive})
    if result: #아이디 패스워드가 동일하고
        print(result)
        if new_receive == nnew_receive: #바꾸려는 비밀번호가 동일하면
            db.login.update_one({'name':username_receive}, {'$set':{'password': new_receive}})
            return jsonify({'result': 'success', 'msg':'수정이 완료되었습니다!'})#db에 비밀번호를 수정하고 로그인 페이지로 되돌아감
        else: #바꾸려는 비밀번호가 동일하지 않으면 -- ssr
            return
    else: #아이디 패스워드가 동일하지 않으면
        print(result)
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


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

# @app.route('/get_time')
# def get_time():
#     return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/edit')
def edit():
    return render_template('edit.html')



@app.route('/timesheet', methods=['POST'])
def getTimesheet():
    divide = request.form['bunluy_give']
    spliting = divide.split('_')

    day = spliting[0]
    bunluy = spliting[1]

    result = list(db.users.find({'bunluy': bunluy, 'day': day}, {'_id': 0}))
    return jsonify({'result': 'success', 'timesheet': result})



if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)

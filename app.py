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
    day=request.form['day_give']
    bunluy=request.form['bunluy_give']

    result = list(db.users.find({'bunluy': bunluy, 'day': day}, {'_id': 0}))
    return jsonify({'result': 'success', 'timesheet': result})



if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)

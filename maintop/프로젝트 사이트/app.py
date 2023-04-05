from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.jungle

app = Flask(__name__)

@app.route('/find', methods=['POST'])
def data():
    day = request.form['day_give']
    bun = request.form['bun_give']

    data = db.users.find({'day': day, 'bunluy': bun})
    data_list = list(data)

    return jsonify({'result': 'success', 'data_list': data_list})

# for day in range(7):
#     for bunlyu in range(3):
#         for time in range(24):      
#             data = {"class":"-", "name":"-", "day": day, "bunlyu": bunlyu,"time": time}
#             db.users.insert_one(data)
day_list = ['일', '월', '화', '수', '목', '금', '토']
bunluy_list = ['세탁기1', '세탁기2', '청소기']
time_list = [i for i in range(24)]

laundry_collection = db['users']
for day in day_list:
    for bunluy in bunluy_list:
        for time in time_list:
            db.users.insert_one({"class":"-", "name":"-", 'day': day, 'bunluy': bunluy, 'time': time})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
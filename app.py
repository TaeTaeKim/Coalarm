from flask import Flask, jsonify, render_template, request
from exchange import exchange
from getdata import corona, embassy, vaccine, kr_name, notice, noticeall, embassy, safe
from mainstatistic import board_data
from pytz import timezone
import json
import datetime
import pymysql
import comment

app = Flask(__name__)
app.register_blueprint(comment.comment)

# 메인 화면
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

# 경보 데이터
@app.route('/data', methods=['GET'])
def data():
    conn = pymysql.connect(host="localhost", user="coalarm", password="v4SxXqsLz", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from Api_Data")
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    lvl_data=[]
    for result in rv:
        lvl_data.append(dict(zip(row_headers,result)))
    conn.close()
    return jsonify({'caution': lvl_data})

# 테이블 데이터
@app.route('/boarddata', methods=['GET'])
def board():
    boarddata = board_data()
    return jsonify(boarddata)

# 안전 점수
@app.route("/safety_score", methods=["GET"])
def safety_score():
    conn = pymysql.connect(host="localhost", user="coalarm", password="v4SxXqsLz", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from Safety_Score order by score desc limit 3")
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    top3_score=[]
    for result in rv:
        top3_score.append(dict(zip(row_headers,result)))
    conn.close()
    return jsonify({"top3_score" : top3_score})

# 상세 페이지
@app.route('/country/<ISO_code>', methods=['GET'])
def country(ISO_code):
    exchange_rate = exchange(ISO_code)
    coronadata = corona(ISO_code)
    vaccinedata = vaccine(ISO_code)
    country_kr = kr_name(ISO_code)
    noticedata = notice(ISO_code)
    allnotice = noticeall(ISO_code)
    embassydata = embassy(ISO_code)
    safedata = safe(ISO_code)
    dataset = {
        'name': country_kr, 'exchange': exchange_rate, 'corona': coronadata,
        'vaccine': vaccinedata, 'notice': noticedata, 'allnotice': allnotice,
        'embassy': embassydata, 'safe': safedata
    }
    return render_template('detail.html', data=dataset)

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True, port=80)

from flask import Flask, jsonify, render_template, request
from exchange import exchange
from getdata import corona, embassy, vaccine, kr_name, notice, noticeall, embassy, safe
from mainstatistic import board_data
from pytz import timezone
import json
import datetime
import pymysql


app = Flask(__name__)

# 메인 화면
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

# 경보 데이터
@app.route('/data', methods=['GET'])
def data():
    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
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
    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
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


# 해당 나라 댓글 개수 알려주기
@app.route('/country/<ISO_code>/comment_update', methods=['GET'])
def get_comment_count(ISO_code):
    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute(f"select count(*) from Comment where iso_code='{ISO_code}';")
    count = cur.fetchall()[0][0]
    conn.close()
    return jsonify({"count" : count})

# 댓글 가져오기
@app.route('/country/<ISO_code>/comment', methods=['GET'])
def comment_data(ISO_code):
    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute(f"select * from Comment c where iso_code='{ISO_code}' order by if(c.parent = -1, idx, parent) desc;")
    row_headers=[x[0] for x in cur.description]
    row_headers[0]="index"
    rv = cur.fetchall()
    comment_data=[]
    for result in rv:
        comment_data.append(dict(zip(row_headers,result)))
    conn.close()
    return jsonify(comment_data)

# 댓글 추가
@app.route('/country/<ISO_code>', methods=['POST'])
def add_comment(ISO_code):    
    data = request.get_json()
    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute('INSERT INTO Comment VALUES(NULL, "{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}")'.format(\
    data["iso_code"], \
    int(data["parent"]), \
    data["text"], \
    data["nickname"], \
    datetime.datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d %H:%M:%S"), \
    data["password"],
    data["class"]))
    conn.commit()
    conn.close()
    return jsonify({"result" : "success"})

# 댓글 수정
@app.route('/country/<ISO_code>', methods=['PATCH'])
def update_comment(ISO_code):
    data = request.get_json()
    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("SELECT password FROM Comment where idx = '{}'".format(data["index"]))
    pw = cur.fetchall()[0][0] 
    if pw == data["password"]:
        cur.execute('UPDATE Comment SET text = "{0}" where idx = "{1}"'.format(data["text"],data["index"]))
        conn.commit()
        conn.close()
        return jsonify({"result": "success"})
    else:
        conn.close()
        return jsonify({"result": "fail"})

# 댓글 삭제
@app.route('/country/<ISO_code>', methods=['DELETE'])
def delete_comment(ISO_code):
    data = request.get_json() 
    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("SELECT password FROM Comment where idx = '{}'".format(data["index"]))
    pw = cur.fetchall()[0][0] 
    if pw == data["password"]:
        cur.execute('DELETE FROM Comment where idx = "{}"'.format(data["index"]))
        cur.execute('DELETE FROM Comment where parent = "{}"'.format(data["index"]))
        conn.commit()
        conn.close()
        return jsonify({"result": "success"})
    else:
        conn.close()
        return jsonify({"result": "fail"})


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True, port=80)

from flask import Blueprint, jsonify, render_template
from blueprint.main_page.mainstatistic import board_data
import pymysql

main_page = Blueprint("main_page", __name__, url_prefix="/")

# 메인 화면
@main_page.route('/', methods=["GET"])
def index():
    return render_template('index.html')

# 경보 데이터
@main_page.route('/data', methods=['GET'])
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
@main_page.route('/boarddata', methods=['GET'])
def board():
    boarddata = board_data()
    return jsonify(boarddata)

# 안전 점수
@main_page.route("/safety_score", methods=["GET"])
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
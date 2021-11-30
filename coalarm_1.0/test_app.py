
# Latest update
# 11/16 flask - mysql 연동 완료

from flask import Flask, jsonify
from exchange import exchange
from getdata import corona, vaccine, kr_name, notice, noticeall
import pymysql
from db_update import db_update

app = Flask(__name__)

corona_update = db_update.AsyncTask()

corona_update.__init__()
# corona_update.update_Corona_Data() # corona update
# corona_update.update_Corona_Vaccine_Data() # vaccine update
# corona_update.update_Api_Data() # api update
# corona_update.update_Embassy_Data() # embassy update
# corona_update.update_Safety_Data() # safety update
# corona_update.update_Safety_Score() # score update
print("db create and update")

@app.route("/")
def home():
    return "hello_world"

@app.route("/corona_data")
def corona_data():
    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from Corona_Data")
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    response_text_dict=[]
    for result in rv:
        response_text_dict.append(dict(zip(row_headers,result)))
    conn.close()
    return jsonify(response_text_dict)
    # conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
    # cur = conn.cursor()
    # cur.execute("select * from Corona_Data")
    # rows = cur.fetchall()
    # conn.close()
    # return jsonify(rows)

@app.route("/corona_vaccine_data")
def corona_vaccine_data():
    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from Corona_Vaccine_Data")
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    response_text_dict=[]
    for result in rv:
        response_text_dict.append(dict(zip(row_headers,result)))
    conn.close()
    return jsonify(response_text_dict)
    # conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
    # cur = conn.cursor()
    # cur.execute("select * from Corona_Vaccine_Data")
    # rows = cur.fetchall()
    # conn.close()
    # return jsonify(rows)

@app.route("/api_data")
def api_data():
    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from Api_Data")
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    response_text_dict=[]
    for result in rv:
        response_text_dict.append(dict(zip(row_headers,result)))
    conn.close()
    return jsonify(response_text_dict)
    # conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
    # cur = conn.cursor()
    # cur.execute("select * from Api_Data")
    # rows = cur.fetchall()
    # conn.close()
    # return jsonify(rows)

@app.route("/embassy_data")
def embassy_data():
    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from Embassy_Data")
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    response_text_dict=[]
    for result in rv:
        response_text_dict.append(dict(zip(row_headers,result)))
    conn.close()
    return jsonify(response_text_dict)
    # conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
    # cur = conn.cursor()
    # cur.execute("select * from Embassy_Data")
    # rows = cur.fetchall()
    # conn.close()
    # return jsonify(rows)

@app.route("/safety_data")
def safety_data():
    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from Safety_Data")
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    response_text_dict=[]
    for result in rv:
        response_text_dict.append(dict(zip(row_headers,result)))
    conn.close()
    return jsonify(response_text_dict)
    # conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
    # cur = conn.cursor()
    # cur.execute("select * from Safety_Data")
    # rows = cur.fetchall()
    # conn.close()
    # return jsonify(rows)

@app.route('/country/<ISO_code>')
def country(ISO_code):
    exchange_rate = exchange(ISO_code)
    coronadata = corona(ISO_code)
    vaccinedata = vaccine(ISO_code)
    country_kr = kr_name(ISO_code)
    noticedata = notice(ISO_code)
    allnotice = noticeall(ISO_code)
    dataset = {
        'name':country_kr,'exchange':exchange_rate,'corona':coronadata,
        'vaccine':vaccinedata,'notice':noticedata,'allnotice':allnotice
        }
    return jsonify(dataset)

if __name__ == "__main__":
    app.run()
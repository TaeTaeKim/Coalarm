# 11/11 변경점
# Entry() -> update_Corona_Data()
# CD() -> update_Corona_Vaccine_Data()
from flask import Flask, jsonify
import pymysql

import db_update

app = Flask(__name__)

corona = db_update.AsyncTask()
corona.update_Corona_Data() # corona_db update
corona.update_Corona_Vaccine_Data() # vaccine_db update
corona.update_Api_Data() # api_db update

# conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
# cur = conn.cursor()
# cur.execute("select * from corona_vaccine_data")
# rows = cur.fetchall()
# conn.close()

@app.route("/")
def home():
    return "hello_world"

@app.route("/corona_data")
def corona_data():
    conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from corona_data")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

@app.route("/corona_vaccine_data")
def corona_vaccine_data():
    conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from corona_vaccine_data")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

@app.route("/api_data")
def api_data():
    conn = pymysql.connect(host="localhost", user="root", password="root", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from api_data")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run()
# 11/11 변경점
# Entry() -> update_Corona_Data()
# CD() -> update_Corona_Vaccine_Data()
from flask import Flask, jsonify
import pymysql

import entry_requirement

app = Flask(__name__)

corona = entry_requirement.AsyncTask()
# corona.update_Corona_Data()
corona.update_Corona_Vaccine_Data() # 백신db 갱신 요청
# corona.update_Api_Data()
conn = pymysql.connect(host="localhost", user="root", password="root")
cur = conn.cursor()
cur.execute("select * from corona_vaccine_data")
rows = cur.fetchall()
for row in rows:
    print(row)
print(type(rows))

@app.route("/")
def home():
    return "hello_world"

if __name__ == "__main__":
    app.run()
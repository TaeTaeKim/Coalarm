# 11/11 변경점
# Entry() -> update_Corona_Data()
# CD() -> update_Corona_Vaccine_Data()
from flask import Flask, jsonify
import sqlite3

import entry_requirement

app = Flask(__name__)

corona = entry_requirement.AsyncTask()
# corona.update_Corona_Data()
corona.update_Corona_Vaccine_Data() # 백신db 갱신 요청

conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute("select * from Corona_Vaccine_Data")
rows = cur.fetchall()
for row in rows:
    print(row)
    {"data" : rows}
print(type(rows))

@app.route("/")
def home():
    return "hello_world"

if __name__ == "__main__":
    app.run()
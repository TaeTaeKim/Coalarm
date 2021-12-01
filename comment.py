from flask import Blueprint, jsonify, request
from pytz import timezone
import datetime
import pymysql

comment = Blueprint("comment", __name__, url_prefix="/")

# 해당 나라 댓글 개수 알려주기
@comment.route('/country/<ISO_code>/comment_update', methods=['GET'])
def get_comment_count(ISO_code):
    conn = pymysql.connect(host="localhost", user="coalarm", password="v4SxXqsLz", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute(f"select count(*) from Comment where iso_code='{ISO_code}';")
    count = cur.fetchall()[0][0]
    conn.close()
    return jsonify({"count" : count})

# 댓글 가져오기
@comment.route('/country/<ISO_code>/comment', methods=['GET'])
def comment_data(ISO_code):
    conn = pymysql.connect(host="localhost", user="coalarm", password="v4SxXqsLz", db="coalarm", charset="utf8")
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
@comment.route('/country/<ISO_code>', methods=['POST'])
def add_comment(ISO_code):    
    data = request.get_json()
    conn = pymysql.connect(host="localhost", user="coalarm", password="v4SxXqsLz", db="coalarm", charset="utf8")
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
@comment.route('/country/<ISO_code>', methods=['PATCH'])
def update_comment(ISO_code):
    data = request.get_json()
    conn = pymysql.connect(host="localhost", user="coalarm", password="v4SxXqsLz", db="coalarm", charset="utf8")
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
@comment.route('/country/<ISO_code>', methods=['DELETE'])
def delete_comment(ISO_code):
    data = request.get_json() 
    conn = pymysql.connect(host="localhost", user="coalarm", password="v4SxXqsLz", db="coalarm", charset="utf8")
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
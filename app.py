from flask import Flask, jsonify, render_template, request
from exchange import exchange
from getdata import corona, embassy, vaccine, kr_name, notice, noticeall, embassy, safe
from mainstatistic import board_data
import json
import datetime
import pymysql


app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/data', methods=['GET'])
def data():
    # with open('./static/Test_json/api_data.json', 'r') as f:
    #     lvl_data = json.load(f)

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


@app.route('/boarddata', methods=['GET'])
def board():
    boarddata = board_data()
    return jsonify(boarddata)

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

@app.route('/country/<ISO_code>', methods=['GET'])
def country(ISO_code):
    # corona_data = Corona_data.query.filter(Coron_data.iso_code = ISO_code).first()
    # vaccine_data = Vaccine_data.query.filter(Vaccine_data.iso_code = ISO_code).first()
    # country_data = {'corona':corona_data,'vaccine':vaccine_data}
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
    # comment table select query
    # with open('./static/Test_json/comment.json', 'r') as f:  # db 업데이트
    #     commentDatas = json.load(f)
    #     result = []
    #     for commentData in commentDatas:
    #         if commentData['iso_code'] == ISO_code:
    #             result.append(commentData)
    # return jsonify(result)
    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("select * from Comment where iso_code='ISO_code' order by parent desc;")
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    comment_data=[]
    for result in rv:
        comment_data.append(dict(zip(row_headers,result)))
    conn.close()

    return jsonify({"count": len(comment_data)})

# db 읽기
@app.route('/country/<ISO_code>/comment', methods=['GET'])
def comment_data(ISO_code):
    # with open('./static/Test_json/comment.json', 'r') as f:
    #     commentDatas = json.load(f)
    #     result = []
    #     for commentData in commentDatas:
    #         if commentData['iso_code'] == ISO_code:
    #             result.append(commentData)
    # return jsonify(result)
    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
    cur = conn.cursor()
    # cur.execute(f"select * from Comment where iso_code='{ISO_code}' order by parent desc;")
    cur.execute(f"select * from Comment c where iso_code='{ISO_code}' order by if(c.parent = -1, idx, parent) desc;")
    row_headers=[x[0] for x in cur.description]
    row_headers[0]="index"
    rv = cur.fetchall()
    comment_data=[]
    for result in rv:
        comment_data.append(dict(zip(row_headers,result)))
    # print(comment_data)
    conn.close()
    return jsonify(comment_data)

# post input : 'iso_code': 'RU', 'parent': -1, 'text': 'asd', 'nickname': 'asd', 'password': 'asd', 'class' : 0 or 1


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
    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
    data["password"],
    data["class"]))

    conn.commit()
    conn.close()
    return jsonify({"result" : "success"})

# update input : 인덱스, 비밀번호, 내용


@app.route('/country/<ISO_code>', methods=['PATCH'])
def update_comment(ISO_code):
    # comment table update query
    # data = request.get_json()
    # with open('./static/Test_json/comment.json', 'r') as f:  # db 대용 json 파일
    #     comment = json.load(f)
    # for i in range(len(comment)):
    #     if data["index"] == comment[i]["index"] and data["password"] == comment[i]["password"]:
    #         comment[i]["write_time"] = datetime.datetime.now().strftime(
    #             "%Y-%m-%d %H:%M:%S")
    #         comment[i]["text"] = data["text"]

    #         # json 파일 저장
    #         # comment = sorted(comment, key=lambda e: (-e['parent'], e['index']))
    #         with open('./static/Test_json/comment.json', 'w') as f:  # db 대용 json 파일
    #             json.dump(comment, f)
    #         return jsonify({"result": "success"})

    # return jsonify({"result": "fail"})

    data = request.get_json()   # {'index': 15, 'text': 'srn', 'password': 'ㅁㄴㅇㄹ'}
    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("SELECT password FROM Comment where idx = '{}'".format(data["index"]))
    pw = cur.fetchall()[0][0] # 가지고 온 비밀번호
    # print(data)
    print(pw, data["password"])
    if pw == data["password"]:
        # print(data)
        print('UPDATE Comment SET text = "{0}" where idx = "{1}"'.format(data["text"],data["index"]))
        cur.execute('UPDATE Comment SET text = "{0}" where idx = "{1}"'.format(data["text"],data["index"]))
        conn.commit()
        conn.close()
        return jsonify({"result": "success"})
    else:
        conn.close()
        return jsonify({"result": "fail"})
    # cur.execute('INSERT INTO Comment VALUES(NULL, "{0}", "{1}", "{2}", "{3}", "{4}", "{5}")'.format(\
    # data[i]["iso_code"], \
    # int(data[i]["parent"]), \
    # data[i]["text"], \
    # data[i]["nickname"], \
    # datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
    # data[i]["password"]))
    # post input : 'iso_code': 'RU', 'parent': -1, 'text': 'asd', 'nickname': 'asd', 'password': 'asd'
    # conn.commit()
    conn.close()
    return jsonify({"result" : "success"})

# delete input : 인덱스, 비밀번호


@app.route('/country/<ISO_code>', methods=['DELETE'])
def delete_comment(ISO_code):
    # comment table delete query
    # data = request.get_json()
    # with open('./static/Test_json/comment.json', 'r') as f:  # db 대용 json 파일
    #     comment = json.load(f)
    # for i in range(len(comment)):
    #     if data["index"] == comment[i]["index"] and data["password"] == comment[i]["password"]:
    #         # 해당 댓글 지우기
    #         comment = list(
    #             filter(lambda x: x["index"] != data["index"], comment))
    #         # 해당 댓글이 부모인 댓글 지우기
    #         comment = list(
    #             filter(lambda x: x["parent"] != data["index"], comment))
    #         # json 파일 저장
    #         comment = sorted(comment, key=lambda e: (-e['parent'], e['index']))
    #         with open('./static/Test_json/comment.json', 'w') as f:  # db 대용 json 파일
    #             json.dump(comment, f)
    #         return jsonify({"result": "success"})

    # return jsonify({"result": "fail"})
    data = request.get_json()   # 'index': 15, 'password': 'ㅁㄴㅇㄹ'
    conn = pymysql.connect(host="localhost", user="coalarm", password="coalarm", db="coalarm", charset="utf8")
    cur = conn.cursor()
    cur.execute("SELECT password FROM Comment where idx = '{}'".format(data["index"]))
    pw = cur.fetchall()[0][0] # 가지고 온 비밀번호
    # print(data)
    # print(pw, data["password"])
    if pw == data["password"]:
        # print(data)
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

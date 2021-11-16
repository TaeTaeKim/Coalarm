from flask import Flask,jsonify,render_template
from exchange import exchange
import json


app = Flask(__name__)
@app.route('/',methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/data',methods=['GET'])
def data():
    with open('./JsonData_main/sample_data.json','r') as f:
        data = json.load(f)

    return jsonify({'result':'success','caution':data})
'''
@app.route('/corona_data',methods=['GET'])
def data():
    with open('./Coalarm_/json_file/corona_data.json','r') as f:
        data = json.load(f)

    return jsonify({'result':'success','caution':data})

@app.route('/corona_vaccine_data',methods=['GET'])
def data():
    with open('./Coalarm_/json_file/corona_data.json','r') as f:
        data = json.load(f)

    return jsonify({'result':'success','caution':data})

@app.route('/api_data',methods=['GET'])
def data():
    with open('./Coalarm_/json_file/corona_data.json','r') as f:
        data = json.load(f)

    return jsonify({'result':'success','caution':data})
'''

@app.route('/country/<ISO_code>', methods=['GET'])
def country(ISO_code):
    # corona_data = Corona_data.query.filter(Coron_data.iso_code = ISO_code).first()
    # vaccine_data = Vaccine_data.query.filter(Vaccine_data.iso_code = ISO_code).first()
    # country_data = {'corona':corona_data,'vaccine':vaccine_data}
    exchange_rate = exchange(ISO_code)
    dataset = {'name':ISO_code,'exchange':exchange_rate}
    return render_template('modal.html',data = dataset)

if __name__ =="__main__":
    app.run(debug=True)

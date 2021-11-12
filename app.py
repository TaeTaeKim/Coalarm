from flask import Flask,jsonify,render_template
import json


app = Flask(__name__)
@app.route('/',methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/data',methods=['GET'])
def home():
    with open('./JsonData_main/sample_data.json','r') as f:
        data = json.load(f)

    return jsonify({'result':'success','caution':data})

if __name__ =="__main__":
    app.run(debug=True)
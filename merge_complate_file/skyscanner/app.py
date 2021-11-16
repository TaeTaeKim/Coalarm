from flask import Flask, request, render_template


app = Flask(__name__)

#API서비스 선언 
@app.route("/", methods=["GET", "POST"]) 
def home():
    if request.method == "POST":
        arrival = request.form['arrival']
        departure = request.form['departure']
        return render_template("Flight_data.html", data = (arrival, departure))
    return render_template("Flight.html")

if __name__ == "__main__":
    app.run(host="localhost", port=5001)
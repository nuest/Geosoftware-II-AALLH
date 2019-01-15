from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route("/")
@app.route("/map")
def webMap():
    return render_template("map.html")

@app.route("/mapTest")
def webMapTest():
    return render_template("mapTest.html")

# @app.route("/getCoordinates", methods = ['POST'])
# def getCoordinates():
#     jsdata = request.form['javascript_data']
#     return jsdata

if __name__ == "__main__":
    app.run()
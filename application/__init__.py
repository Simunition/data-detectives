# __init__.py

import os
from flask import Flask, render_template, Response, request, redirect, url_for, make_response
from werkzeug.utils import secure_filename
import requests

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/"

#MODEL_URL = "http://127.0.0.1:5001"
MODEL_URL = "https://weather-prediction-model-app-de2cee4878db.herokuapp.com"

headings = ("Latitude","Longitude","Variable","Time","Step","Max Wind","Valid Time","met_d")
data = (
    ("-90.0","0.0","gh","2023-01-25 12:00:00","0 days","0.0","2023-01-25 12:00:00","8894.43"),
    ("-28.0","337.5","gh","2023-01-25 12:00:00","0 days","0.0","2023-01-25 12:00:00","12978.59"),
    ("12.5","59.5","gh","2023-01-25 12:00:00","0 days","0.0","2023-01-25 12:00:00","6598.47")
)

@app.route("/")
def home():
    return render_template("home.html", headings=headings, data=data)

@app.route("/gribUpload", methods=['GET','POST'])
def file_upload():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        f_location = app.config['UPLOAD_FOLDER'] + filename
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #file = open(app.config['UPLOAD_FOLDER'] + filename, "r")
        #gribContent = file.read()
        url = MODEL_URL + "/api" #heroku URL needed here
        forecast = requests.post(url, files={'gribFile': open(f_location,'rb')})

    return redirect(request.referrer)

@app.route("/submitCsvOut", methods=['POST'])
def submit_csv_out():
    # get file from request.files
    f = request.files['csvOut']
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
    # save the file to the location
    # return a 200 response with make_response
    return "OK"

@app.route("/submitPngOut", methods=['POST'])
def submit_png_out():
    # get file from request
    f = request.files['pngOut']
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
    with open(app.config['UPLOAD_FOLDER'] + filename, 'rb') as fp:
        png = fp.read()
    return Response(
        png,
        mimetype="image/png",
        headers={"Content-disposition":
                 "attachment; filename=prediction_output.png"})

@app.route("/getCSV")
def getCSV():
    with open("static/prediction_output.csv") as fp:
        csv = fp.read()
   
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=prediction_output.csv"})

@app.route("/getPNG")
def getPNG():
    with open("static/prediction_output.png") as fp:
        csv = fp.read()
   
    return Response(
        csv,
        mimetype="image/png",
        headers={"Content-disposition":
                 "attachment; filename=prediction_output.png"})

if __name__ == "__main__":
    app.run(debug=True)

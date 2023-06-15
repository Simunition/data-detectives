# __init__.py

import os
from flask import Flask, render_template, Response, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/"

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
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #file = open(app.config['UPLOAD_FOLDER'] + filename, "r")
        #gribContent = file.read()

    return redirect(request.referrer)

@app.route("/getCSV")
def getCSV():
    with open("csv_out.csv") as fp:
        csv = fp.read()
   
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=results.csv"})

if __name__ == "__main__":
    app.run(debug=True)
# home.py

from flask import Flask, render_template

app = Flask(__name__)

headings = ("Latitude","Longitude","Variable","Time","Step","Max Wind","Valid Time","met_d")
data = (
    ("-90.0","0.0","gh","2023-01-25 12:00:00","0 days","0.0","2023-01-25 12:00:00","8894.43"),
    ("-28.0","337.5","gh","2023-01-25 12:00:00","0 days","0.0","2023-01-25 12:00:00","12978.59"),
    ("12.5","59.5","gh","2023-01-25 12:00:00","0 days","0.0","2023-01-25 12:00:00","6598.47")
)

@app.route("/")
def home():
    return render_template("home.html", headings=headings, data=data)
    
if __name__ == "__main__":
    app.run(debug=True)
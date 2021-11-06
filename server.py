import time
from datetime import timedelta
from flask import Flask, request, render_template
import flask

app = Flask(__name__, static_folder="public", static_url_path="")

@app.route("/")
def home():
    return flask.render_template("index.html")

@app.route("/RocketLeague")
def RocketLeague():
    return flask.render_template("RocketLeague.html")

@app.route("/LeagueofLegends")
def League():
    return flask.render_template("LeagueofLegends.html")

@app.route("/admin")
def admin():
    return flask.render_template("admin.html")

@app.route("/login")
def login():
    return flask.render_template("login.html")

# === run the server == default port localhost:5000 === (put on heroku to use site live)  
if __name__ == "__main__":
    app.run(debug=True)



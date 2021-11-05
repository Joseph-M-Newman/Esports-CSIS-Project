import time
from datetime import timedelta
from flask import Flask, request, render_template
import flask

app = Flask(__name__, static_folder="public", static_url_path="")
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    return flask.render_template("index.html")
# === run the server == default port localhost:5000 === (put on heroku to use site live)  
if __name__ == "__main__":
    app.run(debug=True)



import time
from datetime import timedelta
from flask import Flask, request, render_template
import flask
import db
from db import DatabaseConnection

app = Flask(__name__, static_folder="public", static_url_path="")
db.populate()

c = DatabaseConnection()


@app.route("/")
def home():
    return flask.render_template("index.html")

@app.route("/RocketLeague")
def RocketLeague():
    c = DatabaseConnection()
    print(c.get_user("joseph"))
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
@app.route("/createAccount")
def createAccount():
    return flask.render_template("createAccount.html")
#add user api
@app.route("/api/adduser", methods=["POST","GET"])
def api_addUser():
    j = request.get_json()
    c = DatabaseConnection()
    response = c.add_user(j["username"], j["password"], False)
    if response == True:
        return {"msg": "Accounted Created"}, 200
    else:
        return {"msg": "Account already exists!"}, 400
# add team api 
@app.route("/api/addteam")
def api_addteam():
    j = request.get_json()
    c = DatabaseConnection()
    response = c.add_team(j["teamname"],j["teamsize"],j["teammembers"])

    if response == True:
        return {"msg": "Team added"}, 200
    else: 
        return {"msg": "Team name already Exists!"}, 400
#login authentication
@app.route("/api/login", methods=["POST"])
def api_login():
    j = request.get_json()
    c = DatabaseConnection()

    auth = check_auth(j,c)

    if auth:
        return auth
    return {"msg":"Successful Authentication"}, 200

def check_auth(j, c):
	if not "username" in j:
		return { "err": "Username must not be empty" }, 400
	if not "password" in j:
		return { "err" : "Password must not be empty" }, 400

	auth = c.auth_user(j["username"], j["password"])

	if auth == None:
		return { "err": "User does not exist" }, 409
	elif auth == False:
		return { "err": "Incorrect password" }, 401

	return None

# === run the server == default port localhost:5000 === (put on heroku to use site live)  
if __name__ == "__main__":
    app.run(debug=True)



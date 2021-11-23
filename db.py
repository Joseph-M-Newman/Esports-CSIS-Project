import sqlite3
import hashlib

DB_NAME = "BallChaser"

# user constants
CREATE_USER_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS user (
	id			INTEGER PRIMARY KEY AUTOINCREMENT,
	username	TEXT UNIQUE NOT NULL,
	pass	TEXT NOT NULL,
	team     TEXT,
	admin		BOOLEAN NOT NULL
);
"""
CREATE_TEAM_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS teams (
	id			INTEGER PRIMARY KEY AUTOINCREMENT,
	teamname		TEXT NOT NULL,
	teamsize		INTEGER,
	teammembers		TEXT
);
"""

DROP_USER_TABLE_QUERY = " DROP TABLE IF EXISTS user"
DROP_TEAM_TABLE_QUERY = "DROP TABLE IF EXISTS teams"

INSERT_USER_QUERY	= "INSERT INTO user (username, pass, admin) VALUES (?, ?, ?)"
DELETE_USER_QUERY	= "DELETE FROM user WHERE username = ?"

INSERT_TEAM_QUERY   = "INSERT INTO teams (teamname, teamsize, teammembers) VALUES (?,?,?)"
DELETE_TEAM_QUERY   = "DELETE FROM teams WHERE teamname = ?"

SELECT_USER_BY_USERNAME_QUERY	= "SELECT * FROM user WHERE username = ?"
SELECT_USER_BY_ID_QUERY	= "SELECT * FROM user WHERE id = ?"
SELECT_USERS_QUERY	= "SELECT * FROM user"

SELECT_TEAM_BY_TEAMANEM_QUERY   = "SELECT * FROM teams WHERE teamname = ?"
SELECT_TEAM_BY_ID_QUERY    = "SELECT * FROM teams WHERE id = ?"
SELECT_TEAM_QUERY   = "SELECT * FROM teams"


UPDATE_TEAMS_QUERY   = "UPDATE teams SET teamname = ?, teamsize = ? , teammembers = ? WHERE id =?"
UPDATE_USER_QUERY	= "UPDATE user SET username = ?, pass = ? WHERE id = ?"

# list constants
CREATE_LIST_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS list (
	id		INTEGER PRIMARY KEY AUTOINCREMENT,
	userid	INTEGER NOT NULL,
	label	TEXT NOT NULL
);
"""
DROP_LIST_TABLE_QUERY = " DROP TABLE IF EXISTS list"

INSERT_LIST_QUERY		= "INSERT INTO list (userid, label) VALUES (?, ?)"
DELETE_LIST_QUERY		= "DELETE FROM list WHERE id = ?"

SELECT_LIST_QUERY		= "SELECT * FROM list WHERE id = ?"
SELECT_USER_LISTS_QUERY	= "SELECT * FROM list WHERE userid = ?"
SELECT_LISTS_QUERY		= "SELECT * FROM list"

class DatabaseConnection:
	
	def __init__(self):
		self.conn = sqlite3.connect(DB_NAME)
		self.init_tables()

	def __del__(self):
		self.conn.close()

	"""
	Gets connection object for db 

	Example Usage:
		conn = db.connect()		# connection object for db
		cur = db.cursor()		# pointer to db data
		some_db_function(cur)	# requires the cursor object from connection
		conn.close()			# ce digest of the data passedoses the connection (very important)

	Params:
		testing		(bool)	if true, changes will not affect db

	Return:
		connection object for db
	"""

	##################################################################
	#	TABLE FUNCTIIONS
	##################################################################

	"""
	Creates tables if they do not exist

	Params:
		cur		(obj)	database cursor
	"""
	def init_tables(self):
		self.conn.execute(CREATE_USER_TABLE_QUERY)
		self.conn.commit()

	"""
	WARNING!
	Deletes all database tables

	Params:
		cur		(obj)	database cursor
	"""
	def clear_database(self):
		self.conn.execute(DROP_USER_TABLE_QUERY)
		self.init_tables()

	##################################################################
	#	USER FUNCTIONS
	##################################################################

	"""
	Adds user to db

	Params:
		cur			(obj)	database cursor
		username	(str)	chosen name of the user
		password	(str)	password for the user
		admin		(bool)	whether or not they have admin privileges
	"""
	def add_user(self, username, password, admin):
		if self.get_user(username):
			return False
		self.conn.execute(INSERT_USER_QUERY, (username, password, admin))
		self.conn.commit()
		return True

	def update_user(self, username, newusername, newpassword):

		if not username:
			return None

		tup = self.conn.execute(SELECT_USER_BY_USERNAME_QUERY, (username,)).fetchone()
		if not tup:
			return None

		if not newusername:
			newusername = username

		self.conn.execute(UPDATE_USER_QUERY, (newusername, newpassword, tup[0]))
		self.conn.commit()

	"""

	Gets all users in user table

	Returns:
		Array of user objects
	"""
	def get_users(self):
		cur = self.conn.execute(SELECT_USERS_QUERY)
		users = []
		for u in cur:
			user = {}
			user["id"] = int(u[0])
			user["username"] = str(u[1])
			user["admin"] = bool(u[3])
			users.append(user)
		return users

	"""
	Gets user from database

	Params:
		username	(str)	username of user

	Return:
		User object if user exists
		None if user doesn't exist
	"""
	def get_user(self, username = "", userid = 0):
		tup = ()
		if not username:
			if not userid:
				return None
			else:
				tup = self.conn.execute(SELECT_USER_BY_ID_QUERY, (userid,)).fetchone()
		else:
			tup = self.conn.execute(SELECT_USER_BY_USERNAME_QUERY, (username,)).fetchone()

		if not tup:
			return None

		user = {}
		user["id"] = int(tup[0])
		user["username"] = str(tup[1])
		user["admin"] = bool(tup[3])
		return user

	"""
	Gets user from database and checks credentials

	Params:
		username	(str)	username of user
		password	(str)	password of user

	Return: 
		True if correct credentials
		False if incorrect password
		None if incorrect username
	"""
	def auth_user(self, username, password):
		user = self.conn.execute(SELECT_USER_BY_USERNAME_QUERY, (username,)).fetchone()
		if user:
			if user[2] == password:
				return True
			else:
				return False
		return None

	def delete_user(self, username):
		u = self.get_user(username)
		if not u:
			return False
		print("user id :", u["id"])
		lists = self.get_lists(u["id"])
		for l in lists:
			self.delete_list(l["id"])
		self.conn.execute(DELETE_USER_QUERY, (username,))
		self.conn.commit()
		return True

############################################################
#		TEAMS FUNCTIONS
############################################################
def add_teams(self, teamname, teamsize, teammembers):
		if self.get_team(teamname):
			return False
		self.conn.execute(INSERT_TEAM_QUERY, (teamname, teamsize, teammembers))
		self.conn.commit()
		return True

def get_team(self, teamname = "", teamid = 0):
		tup = ()
		if not teamname:
			if not teamid:
				return None
			else:
				tup = self.conn.execute(SELECT_TEAM_BY_ID_QUERY, (teamid,)).fetchone()
		else:
			tup = self.conn.execute(SELECT_TEAM_BY_USERNAME_QUERY, (teamname,)).fetchone()

		if not tup:
			return None

		team = {}
		team["id"] = int(tup[0])
		team["teamname"] = str(tup[1])
		team["teamsize"] = bool(tup[3])
		team["teammembers"] = bool(tup[3])
		return team
	
"""
DO NOT CALL THIS FUNCTION
Function to test if everything is working right.
"""
def populate():
	# creating connection object
	conn = DatabaseConnection()
	if conn.get_users():
		print("DB is already initialized. No action taken.")
		return

	print("Populating db with test data")
	
	# dropping all info from db
	# initializing fresh tables
	print("Initializing tables")
	conn.init_tables()

	print("Adding user")
	conn.add_user("joseph","password",False)
	conn.add_user("test","test",True)

if __name__ == "__main__":
	c = DatabaseConnection()
	
	print(c.get_users())
	pass
"""
In this file, the following requirements are covered:
REQ-3.3.3.1: Account Creation
REQ-3.3.3.2: Credential Storage
REQ-3.3.3.3: Credential Modification
REQ-3.3.3.4: Credential Recovery
REQ-3.3.3.5: Login
"""

import sys, os, smtplib, ssl, time, hashlib
sys.path.append('../network')
from .database import Database
from network.email_sender import EmailSender
# from User import User

# @TODO how do we want to do interfaces

class AccountManager:
    """An interface to to manage account operations and sync with database.

    Attributes:
        database (Database) -- Database interface to database file.

    """

    def __init__(self, database_file="database.db"):
        """Initialize an AccountManager.

        """
        print("[account_managers] database_file = {}".format(database_file))
        self.database = Database(database_file)
        self.active_recoveries = {}
        self.recovery_timeout = 10800 # 3 hours (60s/min * 60min/h * 3h)
        self.emailer = EmailSender()
    
    def reset_database(self):
        if os.path.exists(self.database.database_file):
            os.remove(self.database.database_file)
        self.database = Database(self.database.database_file)
        return 0

    def username_available(self, username):
        """Check if a username is already used by someone or if it is available."""
        query = "SELECT * FROM users WHERE username=?"
        data = [username]
        self.database.query(query, data)
        row = self.database.cur.fetchone()
        # print("the row from query is {0}".format(row))
        return 0 if row is None else -1

    def create_account(self, username, password, email):
        """Create an account for a User.

        If provided credentials are valid then create a database entry
        of the new account.

        Keyword arguments:
            username (str) -- User's name
            password (str) -- User's password
            email (str) -- User's email
        """
        # @TODO insert into database
        retval = -1
        if self.username_available(username) != -1:
            # print("username available")
            query = "INSERT INTO users VALUES (?,?,?);"
            data = [username, self.generate_hash(password, username), email]
            self.database.query(query, data)
            retval = 0
        else:
            print("username unavailable")
        return retval

    def set_credentials(self, username, password):
        """Set an account's credentials."""
        # @TODO return values
        query = "UPDATE users SET pwd=? WHERE username=?;"
        data = [self.generate_hash(password, username), username]
        self.database.query(query, data)
        return 0

    def get_credentials(self, username):
        """Get an account's credentials."""
        # @TODO query database
        query = "SELECT * FROM users WHERE username=?"
        data = [username]
        self.database.query(query, data)
        row = self.database.cur.fetchone()
        # process row
        return row

    def login(self, username, password):
        """Validate credentials and provide access to user's resources if valid."""
        # return the user object constructed from database including assets
        # check if credentials match
        query = "SELECT * FROM users WHERE username=? AND pwd=?"
        data = [username, self.generate_hash(password, username)]
        self.database.query(query, data)
        row = self.database.cur.fetchone()
        return row
        # if row is not None:
        #     return row
        # # process row
        # # get other info
        # return -1

    def recover_account(self, username, code, password1, password2):
        """Recover an account's credentials after getting a recovery code."""
        # check if code matches hash of current password
        # if so go to change password
        print("\n\n\n***** trying to recover user {}*****".format(username))
        self.purge_recoveries()
        if username in self.active_recoveries:
            query = "SELECT pwd, email FROM users WHERE username=?"
            data = [username]
            self.database.query(query, data)
            password, email = self.database.cur.fetchone()
            print("passwd, email in recover_account are: {0}, {1}".format(password, email))
            if self.generate_hash(password, self.active_recoveries[username])[:8] == code and password1 == password2:
                print("\n\nrecovery matches\n\n")
                del self.active_recoveries[username]
                self.set_credentials(username, password1)
                return 0
            else:
                print("\n\nrecovery failed:\n\texpected {0} == {1}\t({2})\n\t{3} == {4}\t({5})\n\n".format(self.generate_hash(password, self.active_recoveries[username])[:8], code, self.generate_hash(password, self.active_recoveries[username])[:8] == code, password1, password2, password1 == password2))
        else:
            print("username not in active recoveries")
        return -1

    def generate_hash(self, base, salt=time.time()):
        alg = hashlib.sha256()
        salted = (base + str(salt)).encode('utf-8')
        alg.update(salted)
        return alg.hexdigest()
    
    def purge_recoveries(self):
        """Purge all recovery codes that are expired."""
        for key in self.active_recoveries.copy().keys():
            print("{0} ({1}) - {2} ({3}) = {4}".format(time.time(), type(time.time()), self.active_recoveries[key], type(self.active_recoveries[key]), time.time() - self.active_recoveries[key]))
            if time.time() - self.active_recoveries[key] > self.recovery_timeout:
                print("purging the expired recovery for {0}".format(key))
                del self.active_recoveries[key]


    def send_recovery(self, email):
        """Send a recovery code for user to reset credentials."""
        query = "SELECT username, pwd FROM users WHERE email=?"
        data = [email]
        self.database.query(query, data)
        rows = self.database.cur.fetchall()
        # print("recovery search yielded:{0}".format(row))
        # print("the row from query is {0}".format(row))
        # retval = -1
        if len(rows) != 0:
            print("sending recovery email(s) to {0}".format(rows))
            for recipient in rows:
                salt = time.time()
                code = self.generate_hash(recipient[1], salt)[:8]
                self.active_recoveries[recipient[0]] = salt
                print("added new active recovery, active recoveries is now: {0}".format(self.active_recoveries))
                self.emailer.send_email(email, self.emailer.recovery_body.format(email, recipient[0], code))
            return 0
        else:
            print("email {} not found in database".format(email))
            return -1

    def load_existing_rulesets(self, username):
        """Fetches all existing rulesets"""
        self.database.query("SELECT rulename, rules FROM Ruleset WHERE username = ?", (username, ))
        rows = self.database.cur.fetchall()
        return rows
    
    def create_ruleset(self, username, rulesetName, jsonBlob):
        """Inserts a ruleset into the database."""
        self.database.query("SELECT MAX(ID) FROM Ruleset;", [])
        row = self.database.cur.fetchone()

        if row[0] is None:
            currentIdx = 0
        else: 
            currentIdx = row[0] + 1

        self.database.query("INSERT INTO Ruleset VALUES(?, ?, ?, ?);", (currentIdx, username, rulesetName, jsonBlob,))
        return 0
    
    def update_ruleset(self, username, rulesetName, jsonBlob):
        """Updates an existing ruleset"""
        self.database.query("UPDATE Ruleset SET rules = ? WHERE rulename = ? and username = ?;", (jsonBlob, rulesetName, username, ))
        return 0

    def add_asset(self, username, asset_name, jsonBlob):
        """Inserts an asse"""
        hashname = self.generate_hash(asset_name, username)
        self.database.query("insert into assets values(?, ?, ?, ?);", (hashname, asset_name, username, jsonBlob ))
        return 0

    def update_asset(self, username, asset_name, jsonBlob):
        """Updates an existing asset"""
        hashname = self.generate_hash(asset_name, username)
        self.database.query("update assets image = ? where hashname = ?;", (jsonBlob, hashname))
        return 0

    def get_asset(self, username, asset_name):
        """Get an asset"""
        hashname = self.generate_hash(asset_name, username)
        self.database.query("select image from assets where hashname = ? ;", (hashname,))
        row = self.database.cur.fetchone()
        return row

    def get_assets(self, username):
        """Get all assets for a user"""
        self.database.query("select name, image from assets where username = ?;", (username,))
        rows = self.database.cur.fetchall()
        return rows

    
    # hashname text,
    #                 name text,
    #                 username text,
    #                 image blob,
    #                 primary key (hashname),
    #                 foreign key (username) references users(username)
    def load_game_history(self, username):
        """Fetches game history"""
        self.database.query("SELECT game_id, role, game_name, time FROM GameHistory WHERE username = ?", (username, ))
        rows = self.database.cur.fetchall()
        return rows

    def create_game(self, gameBlob, gameName, username):
        """Creates a game in the database"""
        self.database.query("insert into Game (game) values (?)", (gameBlob, ))
        self.database.query("SELECT MAX(id) from Game;", [])
        gameId = self.database.cur.fetchone()
        if gameId[0] is not None:
            self.database.query("INSERT INTO GameHistory(game_name, role, username, game_id, time) VALUES(?, ?, ?, ?, datetime('now'));", (gameName, "GM", username, gameId[0],))
        else:
            return -1
        return 0
    
    def get_game_id(self, username):
        """Fetches latest game id"""
        self.database.query("SELECT MAX(id) FROM Game;", [])
        row = self.database.cur.fetchone()
        return row
    
    def get_game_history_from_id(self, gameid, username):
        """Fetches latest game id"""
        self.database.query("SELECT game_name FROM GameHistory where game_id = ? and username = ?;", (gameid, username,))
        row = self.database.cur.fetchall()
        return row
    
    def create_game_history_entry(self, gameName, username, gameid):
        """Fetches latest game id"""
        self.database.query("INSERT INTO GameHistory(game_name, role, username, game_id, time) VALUES(?, ?, ?, ?, datetime('now'));", (gameName, "PLAYER", username, gameid, ))
        return 0
    
    def get_list_of_games_and_their_gms(self):
        """Fetches list of games and their gms"""
        self.database.query("SELECT distinct(game_id), username FROM GameHistory;", [])
        rows = self.database.cur.fetchall()
        return rows
    
    def get_game_from_room_number(self, gameId):
        """Fetches game from gameId"""
        self.database.query("SELECT game FROM Game where id = ?;", (gameId, ))
        row = self.database.cur.fetchall()
        return row

    def update_game(self, gameId, gameObj):
        """Updates an existing game"""
        self.database.query("UPDATE Game SET game = ? WHERE id = ?;", (gameObj, int(gameId)))
        return 0
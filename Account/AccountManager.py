"""This module contains the User class."""
import sys
sys.path.append('../')
from .Database import Database
import smtplib, ssl
import time
import hashlib
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
        self.database = Database(database_file)
        self.active_recoveries = {}
        self.recovery_timeout = 10800 # 3 hours (60s/min * 60min/h * 3h)
        self.emailer = EmailSender()

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
            data = [username, password, email]
            self.database.query(query, data)
            retval = 0
        else:
            print("username unavailable")
        return retval

    def set_credentials(self, username, password, email):
        """Set an account's credentials."""
        # @TODO return values
        query = "UPDATE users SET pwd=?, email=? WHERE username=?;"
        data = [password, email, username]
        self.database.query(query, data)

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
        data = [username, password]
        self.database.query(query, data)
        row = self.database.cur.fetchone()
        if row is not None:
            return 0
        # process row
        # get other info
        return -1

    def recover_user(self, username, code, password1, password2):
        """Recover an account's credentials after getting a recovery code."""
        # check if code matches hash of current password
        # if so go to change password
        print("\n\n\n***** trying to recover user *****")
        self.purge_recoveries()
        if username in self.active_recoveries:
            query = "SELECT pwd, email FROM users WHERE username=?"
            data = [username]
            self.database.query(query, data)
            password, email = self.database.cur.fetchone()
            print("passwd, email in recover_user are: {0}, {1}".format(password, email))
            if self.generate_recovery_code(password, self.active_recoveries[username])[:8] == code and password1 == password2:
                print("\n\nrecovery matches\n\n")
                del self.active_recoveries[username]
                self.set_credentials(username, password1, email)
                return 0
            else:
                print("\n\nrecovery failed: expected {0} == {1}\n\n".format(self.generate_recovery_code(password, self.active_recoveries[username])[:8], code))
        else:
            print("username not in active recoveries")
        return -1

    def generate_recovery_code(self, base, salt=time.time()):
        alg = hashlib.sha256()
        salted = (base + str(salt)).encode('utf-8')
        alg.update(salted)
        return alg.hexdigest()
    
    def purge_recoveries(self):
        """Purge all recovery codes that are expired."""
        for key in self.active_recoveries.copy().keys():
            print("{0} ({1}) - {2} ({3}) = {4}".format(self.active_recoveries[key], type(self.active_recoveries[key]), self.recovery_timeout, type(self.recovery_timeout), time.time() - self.active_recoveries[key]))
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
        retval = -1
        if len(rows) != 0:
            print("sending recovery email(s) to {0}".format(rows))
            for recipient in rows:
                salt = time.time()
                code = self.generate_recovery_code(recipient[1], salt)[:8]
                self.active_recoveries[recipient[0]] = salt
                print("added new active recovery, active recoveries is now: {0}".format(self.active_recoveries))
                self.emailer.send_email(email, self.emailer.recovery_body.format(email, recipient[0], code))
            retval = 0
        else:
            print("email {} not found in database".format(email))
        return retval
    
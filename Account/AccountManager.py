"""This module contains the User class."""
import sys
sys.path.append('../')
from .Database import Database
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

    def username_available(self, username):
        """Check if a username is already used by someone or if it is available."""
        query = "SELECT * FROM users WHERE username=?"
        data = [username]
        self.database.query(query, data)
        row = self.database.cur.fetchone()
        print("the row from query is {0}".format(row))
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
            print("username available")
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
        query = "UPDATE users SET pwd=? email=? WHERE username=?;"
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
            return
        # process row
        # get other info
        return row

    def recover_user(self, username, code):
        """Recover an account's credentials after getting a recovery code."""
        # check if code matches hash of current password
        # if so go to change password
        query = "SELECT password FROM users WHERE username=?"
        data = [username]
        self.database.query(query, data)
        row = self.database.cur.fetchone()
        # process the row
        retval = -1
        if code == row + "abc":
            retval = 0
            # go to password reset
        return retval

    def send_recovery(self, email):
        """Send a recovery code for user to reset credentials."""
        query = "SELECT * FROM users WHERE email=?"
        data = [email]
        self.database.query(query, data)
        row = self.database.cur.fetchone()
        print("the row from query is {0}".format(row))
        retval = -1
        if row is not None:
            print("sending recovery email to {}".format(email))
            retval = 0
        else:
            print("email {} not found in database".format(email))
        return retval
        # return 0 if row is None else -1
        # query if email in database
        # generate code (hash their current pass? + salt so diff, but what is salt and is it diff)
        # email code
        # 0 if found email, 1 if not

    # def change_password(self):
    #     """Collect new password for account being recovered."""
    #     self.set_credentials()
    #     return

    # def change_email(self):
    #     """Change the email for an account."""
    #     return

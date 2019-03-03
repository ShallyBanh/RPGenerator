import abc
from Database import Database
from User import User

# @TODO how do we want to do interfaces

class AccountManager:
    def __init__(self):
        self.db = Database("database.db")
    
    def check_all_users(self):
        query = "SELECT * FROM users WHERE username=?"

    def username_available(self, username):
        query = "SELECT * FROM users WHERE username=?"
        data = [username]
        self.db.query(query, data)
        row = self.db.cur.fetchone()
        print("the row from query is {0}".format(row))
        return 0 if row is None else -1

    def create_account(self, username, password, email):
        # @TODO insert into database
        if self.username_available(username) != -1:
            print("username available")
            query = "INSERT INTO users VALUES (?,?,?);"
            data = [username, password, email]
            self.db.query(query, data)
            return 0
        else:
            print("username unavailable")
        return -1
        
    def set_credentials(self, username, password, email):
        return
    
    def get_credentials(self, username):
        # @TODO query database
        return
    
    def update_account(self, username, password, email):
        # how is this different than setCredentials     
        # @TODO update database
        return 
    
    def login(self):
        # check if credentials match
        return
    
    def recover_user(self, username):

        return

    def send_recovery(self):
        return
    
    def reset_login(self):
        return
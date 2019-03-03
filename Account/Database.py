import sqlite3
import os.path

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.cur = None
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self.conn.text_factory = str

        # @TODO crypto
        # create the hash function for passwords
        # self.conn.create_function("hash", 1, encrypt)

        self.cur = self.conn.cursor()

        # enable foreign key constrains
        self.cur.execute(' PRAGMA forteign_keys=ON; ')

        self.create_tables()
        self.conn.commit()

    def create_tables(self):
        # @TODO other tables
        self.cur.execute(
        '''
            create table if not exists users(
                username text,
                pwd text,
                email text,
                primary key (username)
            );
        '''
        )
    
    def query(self, query, data):
        # make sure that data is correct format for query
        print("querying:\n\t{0}\n\t{1}".format(query, data))
        self.cur.execute(query, data)


    def close(self):
        # commit and close cursor at end of session    
        self.conn.commit()
        self.conn.close()
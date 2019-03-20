"""This module contains the User class."""

import sqlite3

class Database:
    """An interface to an SQLite3 database.

    Attributes:
        database_file (str) -- database file to store tables.
        cur (sqlite3.Cursor) -- cursor for the database.
        conn (sqlite3.Connection) -- connection to the database.
        assets (dict) -- User's name. (default empty dict {})

    """

    def __init__(self, database_file):
        """Initialize a Database.

        Keyword arguments:
            database_file (str) -- database file to store tables.
        """
        self.database_file = database_file
        self.conn = sqlite3.connect(self.database_file, check_same_thread=False)
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
        """Create the tables in the database if they do not already exist."""
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
        self.cur.execute(
            '''
                create table if not exists assets(
                    hashname text,
                    name text,
                    username text,
                    image blob,
                    primary key (hashname),
                    foreign key (username) references users(username)
                );
            '''
        )
        self.cur.execute(
            '''
                create table if not exists Ruleset(
                    id integer,
                    username text,
                    rules blob,
                    primary key (id),
                    foreign key (username) references users(username)
                );
            '''
        )
        self.cur.execute(
            '''
                create table if not exists GameHistory(
                    id integer,
                    role text,
                    username text,
                    game_id integer,
                    primary key (id),
                    foreign key (username) references users(username),
                    foreign key (game_id) references Game(id)
                );
            '''
        )
        self.cur.execute(
            '''
                create table if not exists Game(
                    id integer,
                    game blob,
                    primary key (id)
                );
            '''
        )

    def query(self, query, data):
        """Query the database with query using arguments in data."""
        # make sure that data is correct format for query
        # print("querying:\n\t{0}\n\t{1}".format(query, data))
        self.cur.execute(query, data)

    def close(self):
        """Close the connection to the database."""
        # commit and close cursor at end of session
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    database = Database("test.db")

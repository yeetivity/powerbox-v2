"""
Module responsible for all communication with the SQLite3 database

Author: Jitse van Esch
Date: 24-03-23
"""

import logging
import sqlite3
from sqlite3 import Error

class Database():
    def __init__(self, db):
        """ Create a database connection to a SQLite database"""

        # Initialize connection
        self.conn = None
        try:
            # Create connection
            self.conn = sqlite3.connect(db)
            logging.info("Successfully connected to database using SQLite version: %s", sqlite3.version)

            # Create a cursor (allows to execution of SQL statements)
            self.cur = self.conn.cursor()

            # Check if tables exist; if not they are created
            self.tablecheck()

        except Error as e:
            logging.error("Error connecting to database: %s", e)

    def tablecheck(self):
        """
        Function to check if all needed tables exist
        """
        # user table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                userID INTEGER PRIMARY KEY,
                firstname varchar(255),
                lastname varchar(255),
                sport varchar(255),
                gender varchar(255),
                height int
            )
        """)

        # result table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS results (
                resultID INTEGER PRIMARY KEY,
                userID int,
                weight double,
                pushheight int,
                date varchar(255)
            )
        """)

        # personal best table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS pbs (
                userID INTEGER PRIMARY KEY,
                peakforce double,
                meanforce double,
                timetopeakforce double,
                best_rfd double,
                power_avg double,
                velocity_avg double,
                distance double,
                peak_acc double,
                fatigability int,
                timetofatigue double
            )
        """)

        # commit to database
        self.conn.commit()
        return

    def get_users(self, gender=None, sport=None):
        """
        Function to get users from the database

        Args:
            gender (str, optional): Filter users based on gender. Defaults to None.
            sport (str, optional): Filter users based on sport. Defaults to None.

        Returns:
            List of tuples containing user information.
        """
        query = "SELECT * FROM users"
        args = ()

        if gender is not None and sport is not None:
            query += " WHERE gender=? AND sport=?"
            args = (gender, sport)
        elif gender is not None:
            query += " WHERE gender=?"
            args = (gender,)
        elif sport is not None:
            query += " WHERE sport=?"
            args = (sport,)

        self.cur.execute(query, args)
        result = self.cur.fetchall()
        return result

    def get_userdetails(self, usrID):
        """Function to get all details for a specific user"""
        
        query = "SELECT * FROM users WHERE userID = ?"
        params = (usrID,)
        try:
            self.cur.execute(query, params)
            result = self.cur.fetchone()
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
        
        return result
    
    def get_userresults(self, usrID):
        query = "SELECT * FROM results WHERE userID = ?"
        params = (usrID,)
        try:
            self.cur.execute(query, params)
            result = self.cur.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
        
        return result
    
    def get_userpbs(self, usrID):
        query = "SELECT * FROM pbs WHERE userID = ?"
        params = (usrID,)
        try:
            self.cur.execute(query, params)
            result = self.cur.fetchone()
            if result == None:
                # No personal bests are recorded yet
                print('No personal bests found, creating entry....')
                self.add_personalbestentry(usrID)
                self.cur.execute(query, params)
                result = self.cur.fetchone()
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
        
        return result

    def add_user(self, userdetails):
        """ Function to add a new user to the database """
        firstname, lastname = userdetails[0].split(" ", 1)
        sport, gender, height = userdetails[1:4]

        self.cur.execute("""
            INSERT INTO users (firstname, lastname, sport, gender, height) 
            SELECT ?, ?, ?, ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM users WHERE firstname = ? AND lastname = ?)
            """,
            (firstname, lastname, sport, gender, height, firstname, lastname))
        userID = self.cur.lastrowid
        print(userID)
        self.conn.commit()
        return userID
    
    def add_personalbestentry(self, usrID):
        self.cur.execute("""
            INSERT INTO pbs VALUES (?, 0, 0, 100000, 0, 0, 0, 0, 0, 0, 100000)
            """, (usrID,))
        self.conn.commit()
        return

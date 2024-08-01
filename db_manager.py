# db_manager.py

import sqlite3
from config import database

class DB_Manager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        try:
            con = sqlite3.connect(self.database)
            con.execute('PRAGMA foreign_keys = ON;')
            with con:
                # Create the Car table
                con.execute('''CREATE TABLE IF NOT EXISTS Car (
                    car_id INTEGER PRIMARY KEY,
                    car_brand TEXT,
                    color TEXT,
                    year INTEGER
                )''')

                # Create the CarPark table
                con.execute('''CREATE TABLE IF NOT EXISTS CarPark (
                    car_park_id INTEGER PRIMARY KEY,
                    car_park_name TEXT
                )''')

                # Create the Cars_Id table with foreign keys
                con.execute('''CREATE TABLE IF NOT EXISTS Cars_Id (
                    cars_park_id INTEGER,
                    car_id INTEGER,
                    FOREIGN KEY(cars_park_id) REFERENCES CarPark(car_park_id),
                    FOREIGN KEY(car_id) REFERENCES Car(car_id)
                )''')
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

# Example usage
if __name__ == '__main__':
    db_manager = DB_Manager(database)
    db_manager.create_tables()

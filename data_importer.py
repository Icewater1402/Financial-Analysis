import sqlite3
import csv
import os.path 

class DataImporter:
    def __init__(self, csv_file_path, db_file_path):
        self.csv_file_path = csv_file_path 
        self.db_file_path = db_file_path 
    
    def import_data(self):
        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()

        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='finance_table'")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                CREATE TABLE finance_table (
                           Date TEXT,
                           Post_Date TEXT,
                           Description TEXT, 
                           Category TEXT,
                           Type TEXT,
                           Amount DOUBLE,
                           Memo TEXT
                           )
                           ''')
            conn.commit()
            with open(self.csv_file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)  # Skip the header row if there is one

                for row in csv_reader:
                    cursor.execute('''
                        INSERT INTO finance_table (Date, Post_Date, Description, Category, Type, Amount, Memo)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', row)

                conn.commit()
                
        else:
            print("Table 'finance_table' already exists. Skipping creation and data insertion.")
        conn.close()

    def drop_table(self):
        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS finance_table")
        conn.commit()
        conn.close()
                           
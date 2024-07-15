import sqlite3
import csv
import os.path

# Step 1: Connect to SQLite database (or create it if it doesn't exist)
db_file = 'finances.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Check if finance_table already exists
cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='finance_table'")
if cursor.fetchone()[0] == 0:
    # Step 2: Create table if it doesn't exist
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

    # Step 3: Read CSV file and insert data into finance_table
    csv_file_path = 'Chase4950_Activity20220715_20240715_20240715.CSV'

    with open(csv_file_path, 'r') as csv_file:
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

# Example query
cursor.execute('''
    SELECT SUM(Amount) AS TotalFoodSpending
    FROM finance_table
    WHERE Category = 'Food & Drink'
''')
result = cursor.fetchone()
print("Total Entertainment Spending (Food & Drink):", result[0])

cursor.execute('''
    SELECT SUM(Amount) AS EntertainmentSpending
    FROM finance_table
    WHERE Category = 'Entertainment'
''')
result = cursor.fetchone()
print("Total Entertainment Spending (Entertainment):", result[0])

# Close the connection
conn.close()

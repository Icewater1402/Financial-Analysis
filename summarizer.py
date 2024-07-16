import sqlite3

class Summarizer:
    def __init__(self, db_file_path):
        self.db_file_path = db_file_path
    
    def get_total_spending_by_category(self, category):
        # Connect to SQLite database
        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()

        # Query total spending in the specified category
        cursor.execute('''
            SELECT SUM(Amount) AS TotalSpending
            FROM finance_table
            WHERE Category = ?
        ''', (category,))
        
        result = cursor.fetchone()
        total_spending = result[0] if result[0] else 0.0
        
        # Close the connection
        conn.close()
        
        return total_spending

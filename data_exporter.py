import csv
import sqlite3
from datetime import datetime
import pandas as pd

class DataExporter:
    def __init__(self, db_file_path):
        self.db_file_path = db_file_path
    
    def export_monthly_spending(self, output_file_path):
        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()

        # Query to select the necessary data
        query = '''SELECT Date, Amount FROM finance_table WHERE Amount < 0'''  # Assuming negative values are expenses
        cursor.execute(query)
        rows = cursor.fetchall()

        conn.close()

        # Convert the data into a pandas DataFrame for easier manipulation
        data = pd.DataFrame(rows, columns=['Date', 'Amount'])

        # Convert 'Date' to a datetime object and extract month and year
        data['Date'] = pd.to_datetime(data['Date'])
        data['Year-Month'] = data['Date'].dt.to_period('M')

        # Group by Year-Month and calculate total and average spending
        monthly_spending = data.groupby('Year-Month').agg(
            total_spending=('Amount', 'sum'),
            average_spending=('Amount', 'mean')
        ).reset_index()

        # Create a mapping of year-month to full month names
        monthly_spending['Month'] = monthly_spending['Year-Month'].dt.month
        monthly_spending['Year'] = monthly_spending['Year-Month'].dt.year
        monthly_spending['Month'] = monthly_spending['Month'].apply(lambda x: datetime(2024, x, 1).strftime('%B'))  # Get full month name

        # Pivot the DataFrame to have month names as columns
        monthly_spending_pivot = monthly_spending.pivot_table(
            index='Year',  # Using 'Year' as the index
            columns='Month',
            values='total_spending',
            fill_value=0
        )

        # Calculate average spending per month for the 'Average Spending' row
        average_spending_values = monthly_spending.groupby('Month')['average_spending'].mean().reindex(monthly_spending_pivot.columns, fill_value=0)

        # Create a Series for the average spending row with correct index
        monthly_spending_pivot.loc['Average Spending'] = average_spending_values

        # Reset the index to ensure proper alignment
        monthly_spending_pivot.reset_index(drop=False, inplace=True)

        # Check the output file path's extension and save accordingly
        if output_file_path.endswith('.xlsx'):
            monthly_spending_pivot.to_excel(output_file_path, index=False)
        elif output_file_path.endswith('.csv'):
            monthly_spending_pivot.to_csv(output_file_path, index=False)
        else:
            raise ValueError("Unsupported file format. Please use '.xlsx' for Excel or '.csv' for CSV.")

        print(f"Data exported to {output_file_path}")



# Usage
db_file_path = 'finances.db'
output_file_path = 'monthly_spending.xlsx'

exporter = DataExporter(db_file_path)
exporter.export_monthly_spending(output_file_path)

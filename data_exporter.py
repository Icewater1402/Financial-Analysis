import sqlite3
import pandas as pd
from datetime import datetime

class DataExporter:
    def __init__(self, db_file_path, essentials):
        self.db_file_path = db_file_path
        self.essentials = essentials  # Store essentials list

    def export_transactions_to_excel(self, output_file_path):
        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()

        # Query to select all transaction data
        query = '''SELECT Date, Description, Category, Amount FROM finance_table'''  # Include category
        cursor.execute(query)
        rows = cursor.fetchall()

        conn.close()

        # Convert the data into a pandas DataFrame for easier manipulation
        data = pd.DataFrame(rows, columns=['Date', 'Description', 'Category', 'Amount'])

        # Convert 'Date' to a datetime object and extract month and year
        data['Date'] = pd.to_datetime(data['Date'])
        data['Year-Month'] = data['Date'].dt.to_period('M')

        # Create a Pandas Excel writer using XlsxWriter as the engine
        with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
            # Create monthly spending summary
            monthly_summary = data[data['Amount'] < 0].groupby(data['Year-Month']).agg(
                total_spending=('Amount', 'sum'),
                average_spending=('Amount', 'mean')
            ).reset_index()

            # Format month names for summary
            monthly_summary['Month'] = monthly_summary['Year-Month'].dt.month
            monthly_summary['Year'] = monthly_summary['Year-Month'].dt.year
            monthly_summary['Month'] = monthly_summary['Month'].apply(lambda x: datetime(2024, x, 1).strftime('%B'))  # Get full month name

            # Pivot the DataFrame to have month names as columns
            summary_pivot = monthly_summary.pivot_table(
                index='Year',  # Using 'Year' as the index
                columns='Month',
                values='total_spending',
                fill_value=0
            )

            # Add average spending as an additional row
            average_spending_values = monthly_summary.groupby('Month')['average_spending'].mean().reindex(summary_pivot.columns, fill_value=0)
            summary_pivot.loc['Average Spending'] = average_spending_values
            summary_pivot.reset_index(drop=False, inplace=True)

            # Write summary to a new sheet
            summary_pivot.to_excel(writer, sheet_name='Monthly Summary', index=False)
            # Export transactions to individual sheets by month
            for month, group in data.groupby(data['Year-Month']):
                month_name = month.strftime('%Y-%m')  # Format to 'YYYY-MM'
                group.to_excel(writer, sheet_name=month_name, index=False)


            # Calculate totals for the essentials categories for the snapshot sheet
            snapshot_data = {essential: 0 for essential in self.essentials}

            # Sum the amounts for each essential category
            for essential in self.essentials:
                total = data[data['Category'] == essential]['Amount'].sum()
                snapshot_data[essential] = total

            # Prepare snapshot DataFrame with categories as rows
            snapshot_df = pd.DataFrame(list(snapshot_data.items()), columns=['Category', 'Total'])

            # Create a summary DataFrame for total spending
            total_spending = data['Amount'].sum()
            total_df = pd.DataFrame({
                'Category': ['Total Spending'],
                'Total': [total_spending]
            })

            # Combine total_df and snapshot_df
            final_df = pd.concat([total_df, snapshot_df], ignore_index=True)

            # Write the final DataFrame to a new sheet
            final_df.to_excel(writer, sheet_name='Snapshot', index=False)

        print(f"Data exported to {output_file_path}")

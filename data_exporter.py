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
        data['Year'] = data['Date'].dt.year
        data['Month'] = data['Date'].dt.month_name()

        # Create a Pandas Excel writer using XlsxWriter as the engine
        with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
            # Get unique years from the data
            unique_years = data['Year'].unique()

            # Loop through each year and create a separate Monthly Summary sheet
            for year in unique_years:
                # Create Monthly Summary sheet for each year (e.g., "Monthly Summary 2022")
                monthly_summary_sheet = writer.book.add_worksheet(f'Monthly Summary {year}')

                # Setup titles in the first row (B1 as "Average", C1 as "Total", and months in D1-M1)
                monthly_summary_sheet.write('A1', 'Snapshot')
                monthly_summary_sheet.write('B1', 'Average')
                monthly_summary_sheet.write('C1', 'Total')

                # Write month names in D1 to O1
                months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                for col_num, month in enumerate(months, start=3):
                    monthly_summary_sheet.write(0, col_num, month)

                # Write the categories in column A
                categories = [
                    "Paychecks", "", "", "Total Spending", "", "", "Essentials", 
                    "Rent/Mortgage", "Car Payment", "Car Insurance", "Joe Life Insurance", 
                    "Internet", "Parents", "----------------", "Utilities", "Gasoline", 
                    "Grocery", "Other Bills", "", "Special", "", "Leisure", "W/o Special", "", 
                    "Difference", "", "Savings"
                ]
                for row_num, category in enumerate(categories, start=1):
                    monthly_summary_sheet.write(row_num, 0, category)

                # Initialize all cells with zero for the specific year
                for row_num in range(1, len(categories) + 1):
                    for col_num in range(1, 13):  # Columns B to O for the months
                        if row_num == 2 or row_num == 3 or row_num == 5 or row_num == 6 or row_num == 14 or row_num == 19 or row_num == 21 or row_num == 23: #hard coded for format
                            monthly_summary_sheet.write(row_num, col_num, "")
                        else:
                            monthly_summary_sheet.write(row_num, col_num, 0)

                # Apply some basic formatting
                header_format = writer.book.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
                monthly_summary_sheet.set_row(0, None, header_format)  # Bold headers in the first row
                monthly_summary_sheet.set_column('A:A', 20)  # Set the category column width
                monthly_summary_sheet.set_column('B:O', 12)  # Set the month columns' width

                # Make the separator row greyed out
                grey_format = writer.book.add_format({'bg_color': '#D3D3D3'})
                monthly_summary_sheet.set_row(14, None, grey_format)  # "----------------" row in grey


            # Now let's add the Monthly Spending summary sheet
            monthly_summary_sheet.write('B2', 0)  # Placeholder for average values
            monthly_summary_sheet.write('C2', 0)  # Placeholder for total values

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

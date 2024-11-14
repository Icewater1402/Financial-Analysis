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
            years = data['Year'].unique()

            for year in years:
                # Filter data by the current year
                yearly_data = data[data['Year'] == year]

                # Create a summary DataFrame for total spending and essentials for the Monthly Spending sheet
                snapshot_data = {
                    'paychecks': 0,
                    'Total Spending': yearly_data[yearly_data['Amount'] < 0]['Amount'].sum(),  # This will have months in the second row
                    'Essentials': {essential: 0 for essential in self.essentials},
                    'Savings': 0,
                    'special': 0,
                    'leisure': 0,
                    'w/o special': 0,
                    'difference': 0
                }

                # Sum the amounts for each essential category
                for essential in snapshot_data['Essentials']:
                    snapshot_data['Essentials'][essential] = yearly_data[yearly_data['Category'] == essential]['Amount'].sum()

                # Prepare snapshot DataFrame with categories as rows
                essentials_data = [(key, value) for key, value in snapshot_data['Essentials'].items()]
                snapshot_df = pd.DataFrame({
                    'Category': ['paychecks', 'Total Spending'] + [item[0] for item in essentials_data] + ['Savings', 'special', 'leisure', 'w/o special', 'difference'],
                    'Total': [snapshot_data['paychecks'], snapshot_data['Total Spending']] + [item[1] for item in essentials_data] + [snapshot_data['Savings'], snapshot_data['special'], snapshot_data['leisure'], snapshot_data['w/o special'], snapshot_data['difference']]
                })

                # Insert blank rows
                blank_row = pd.DataFrame([[''] * len(snapshot_df.columns)], columns=snapshot_df.columns)
                snapshot_df = pd.concat([snapshot_df.iloc[:2], blank_row, snapshot_df.iloc[2:6], blank_row, snapshot_df.iloc[6:]], ignore_index=True)

                # Create additional columns for each month (January to December)
                months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                
                # Add months columns initialized with zero
                for month in months:
                    month_data = yearly_data[(yearly_data['Month'] == month) & (yearly_data['Amount'] < 0)]
                    for index, row in snapshot_df.iterrows():
                        category = row['Category']
                        if category in self.essentials:
                            snapshot_df.at[index, month] = month_data[month_data['Category'] == category]['Amount'].sum()

                # Write the snapshot data to a new sheet (year-specific Monthly Spending sheet)
                snapshot_df.to_excel(writer, sheet_name=f'{year} Monthly Spending', index=False, startrow=1)

                # Add formatting to the Monthly Spending sheet to match the layout
                workbook = writer.book
                snapshot_sheet = writer.sheets[f'{year} Monthly Spending']

                # Bold the 'Essentials' row
                snapshot_sheet.write('A8', 'Essentials', workbook.add_format({'bold': True}))

                # Adjust column widths for readability
                snapshot_sheet.set_column('A:A', 20)  # 'Category' column
                snapshot_sheet.set_column('B:B', 10)  # 'Total' column
                snapshot_sheet.set_column('C:N', 10)  # Months columns (January to December)

                # Write the header for monthly columns (Jan-Dec) in row 2
                snapshot_sheet.write_row('C2', months)  # Put month names in the second row
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

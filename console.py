import tkinter as tk
from tkinter import filedialog
from data_importer import DataImporter
from summarizer import Summarizer
from data_exporter import DataExporter

class Console:
    def __init__(self):
        self.db_file_path = 'finances.db'
        self.data_importer = None
        self.summarizer = None

    def run(self):
        while True:
            print("\n=== Financial Data Manager ===")
            print("1. Import CSV Data")
            print("2. Summarize Category Spending")
            print("3. Display All Spending Categories")
            print("4. Display Expenses by Category")
            print("5. Create Pie Chart of Spending")
            print("6. Create Line Graph of Spending")
            print("7. Export Monthly Spending")
            print("8. Clear All Data")
            print("0. Exit")
            
            choice = input("Please choose an option: ")

            if choice == '1':
                self.import_csv_data()
            elif choice == '2':
                if self.summarizer:
                    self.summarizer.summarize_category_spending()
                else:
                    print("No CSV data imported yet.")
            elif choice == '3':
                if self.summarizer:
                    self.summarizer.display_all_categories()
                else:
                    print("No CSV data imported yet.")
            elif choice == '4':
                if self.summarizer:
                    self.summarizer.display_expenses_by_category()
                else:
                    print("No CSV data imported yet.")
            elif choice == '5':
                if self.summarizer:
                    self.summarizer.create_pie_chart()
                else:
                    print("No CSV data imported yet.")
            elif choice == '6':
                if self.summarizer:
                    self.summarizer.create_line_graph()
                else:
                    print("No CSV data imported yet.")
            elif choice == '7':
                self.export_monthly_spending()
            elif choice == '8':
                if self.data_importer:
                    self.data_importer.drop_table()
                    print("All data cleared from the database.")
                else:
                    print("No data imported yet.")
            elif choice == '0':
                print("Exiting program.")
                break
            else:
                print("Invalid option. Please try again.")

    def export_monthly_spending(self):
        output_file_path = filedialog.asksaveasfilename(
            title="Save Monthly Spending Report",
            defaultextension=".xlsx",
            filetypes=(("CSV files", "*.xlsx"), ("All files", "*.*"))
        )
        
        if not output_file_path:
            print("No file selected. Exiting.")
            return

        exporter = DataExporter(self.db_file_path)
        exporter.export_transactions_to_excel(output_file_path)
    
    def import_csv_data(self):
        # Hide the root window
        root = tk.Tk()
        root.withdraw()  

        # Open file dialog to select the CSV file
        csv_file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )

        if not csv_file_path:
            print("No file selected.")
            return

        # Initialize DataImporter and import data
        self.data_importer = DataImporter(csv_file_path, self.db_file_path)
        self.data_importer.import_data()

        # Initialize Summarizer after data import
        self.summarizer = Summarizer(self.db_file_path)
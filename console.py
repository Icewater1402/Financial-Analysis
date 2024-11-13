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
            print("2. Select Essentials Categories")
            print("3. Summarize Category Spending")
            print("4. Display All Spending Categories")
            print("5. Display Expenses by Category")
            print("6. Create Pie Chart of Spending")
            print("7. Create Line Graph of Spending")
            print("8. Export Monthly Spending")
            print("9. Clear All Data")
            print("0. Exit")
            
            choice = input("Please choose an option: ")

            if choice == '1':
                self.import_csv_data()
            elif choice == '2':
                self.select_essentials()
            elif choice == '3':
                if self.summarizer:
                    self.summarizer.summarize_category_spending()
                else:
                    print("No CSV data imported yet.")
            elif choice == '4':
                if self.summarizer:
                    self.summarizer.display_all_categories()
                else:
                    print("No CSV data imported yet.")
            elif choice == '5':
                if self.summarizer:
                    self.summarizer.display_expenses_by_category()
                else:
                    print("No CSV data imported yet.")
            elif choice == '6':
                if self.summarizer:
                    self.summarizer.create_pie_chart()
                else:
                    print("No CSV data imported yet.")
            elif choice == '7':
                if self.summarizer:
                    self.summarizer.create_line_graph()
                else:
                    print("No CSV data imported yet.")
            elif choice == '8':
                self.export_monthly_spending()
            elif choice == '9':
                if self.data_importer:
                    self.data_importer.drop_table()
                    print("All data cleared from the database.")
                    self.data_importer = None
                    self.summarizer = None
                else:
                    print("No data imported yet.")
            elif choice == '0':
                print("Exiting program.")
                break
            else:
                print("Invalid option. Please try again.")
    
    def select_essentials(self):
        if not self.summarizer:
            print("No CSV data imported yet.")
            return 
        
        all_categories = self.summarizer.get_all_categories()
        print("Available Categories: ")
        for indx, category in enumerate(all_categories, start = 1):
            print(f"{indx}. {category}")
        
        selected_indices = input("Select essential categories by numbers (comma-separated): ")
        selected_indices = selected_indices.split(',')

        self.essentials = [all_categories[int(index) - 1] for index in selected_indices if index.isdigit() and 0 < int(index) <= len(all_categories)]
        print("Selected Essentials:", self.essentials)

    def export_monthly_spending(self):
        output_file_path = filedialog.asksaveasfilename(
            title="Save Monthly Spending Report",
            defaultextension=".xlsx",
            filetypes=(("CSV files", "*.xlsx"), ("All files", "*.*"))
        )
        
        if not output_file_path:
            print("No file selected. Exiting.")
            return

        exporter = DataExporter(self.db_file_path, self.essentials)
        exporter.export_transactions_to_excel(output_file_path)
    
    def import_csv_data(self):
        # Hide the root window
        root = tk.Tk()
        root.withdraw() 
        root.lift() 

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
import tkinter as tk
from tkinter import filedialog
from data_importer import DataImporter
from summarizer import Summarizer

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog to select the CSV file
    csv_file_path = filedialog.askopenfilename(
        title="Select CSV file",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )

    if not csv_file_path:
        print("No file selected. Exiting.")
        return

    # Database file path
    db_file_path = 'finances.db'

    # Initialize DataImporter and import data if the table doesn't exist
    data_importer = DataImporter(csv_file_path, db_file_path)
    data_importer.import_data()

    # Initialize Summarizer
    summarizer = Summarizer(db_file_path)
    
    summarizer.summarize_category_spending()
    summarizer.display_all_categories()
    summarizer.display_expenses_by_category()

    
    summarizer.create_pie_chart()
    summarizer.create_line_graph()
    

    data_importer.drop_table()

if __name__ == '__main__':
    main()

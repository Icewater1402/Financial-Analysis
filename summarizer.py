import sqlite3
import matplotlib.pyplot as plt
import pandas as pd 

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
    
    def summarize_category_spending(self):
        #gives a breakdown of all totals in each category
        total_food_spending = self.get_total_spending_by_category('Food & Drink') #Food and Drink
        print("Total Food Spending:", total_food_spending)
    
        total_entertainment_spending = self.get_total_spending_by_category('Entertainment') #Entertainment 
        print("Total Entertainment Spending:", total_entertainment_spending)

        total_gas_spending = self.get_total_spending_by_category('Gas') #Gas
        print("Total Gas Spending:", total_gas_spending)

        total_gas_spending = self.get_total_spending_by_category('Health & Wellness') #Health and Wellness
        print("Total Health and Wellness Spending:", total_gas_spending)

        total_gas_spending = self.get_total_spending_by_category('Education') #Education
        print("Total Education Spending:", total_gas_spending)

        total_gas_spending = self.get_total_spending_by_category('Travel') #Travel
        print("Total Travel Spending:", total_gas_spending)

        total_gas_spending = self.get_total_spending_by_category('Groceries') #Groceries
        print("Total Groceries Spending:", total_gas_spending)

    def get_all_categories(self):
        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()

        cursor.execute('''
                       SELECT DISTINCT Category
                       FROM finance_table
                       ''')
        categories = cursor.fetchall()

        conn.close()

        return [category[0] for category in categories if category[0]]
    
    def display_all_categories(self):
        categories = self.get_all_categories()

        if not categories:
            print("No categories found.")
            return
        print("Existing Categories")
        for category in categories:
            print(f"- {category}")
        
    def get_all_category_totals(self):
        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT Category, SUM(Amount) AS TotalSpending
            FROM finance_table
            GROUP BY Category
            ''')
        results = cursor.fetchall()
        conn.close()

        return results
    
    def get_expenses_by_category(self, category):

        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()

        cursor.execute('''
                       SELECT Date, Description, Amount
                       FROM finance_table
                       WHERE Category = ? AND Amount < 0
                       ''',(category,))
        expenses = cursor.fetchall()

        conn.close()

        if not expenses:
            print(f"No expenses were found for category: {category}")
            return[]
        return expenses
    
    def display_expenses_by_category(self):
        category = input("Enter the category you'd like to see expenses for: ")
        expenses = self.get_expenses_by_category(category)

        if expenses:
            print(f"Expenses under the category '{category}': ")
            for date, description, amount in expenses:
                print(f"Date: {date}, Description: {description}, Amount: ${abs(amount):.2f}")  # Display positive value
    
    def get_all_data(self):
        conn = sqlite3.connect(self.db_file_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM finance_table')
        data = cursor.fetchall()

        conn.close()

        return data

    def create_pie_chart(self):
        data = self.get_all_category_totals()
        
        if not data:
            print("No data available to plot.")
            return
        
        # Separate data into categories and amounts
        categories, amounts = zip(*data)
        
        # Statements include money put back into the card, filter EXPENSES only
        filtered_data = [(cat, abs(amt)) for cat, amt in zip(categories, amounts) if amt < 0]
        
        if not filtered_data:
            print("No expense data available to plot.")
            return

        filtered_categories, filtered_amounts = zip(*filtered_data)
        
        # Pie chart creation
        fig, ax = plt.subplots(figsize=(10, 8))  # Increase figure size if needed
        
        # Fonts and Labels
        textprops = {'fontsize': 10}  # Set the desired font size for labels and percentages
        wedges, texts, autotexts = ax.pie(filtered_amounts, labels=filtered_categories, autopct='%1.1f%%',
                                        textprops=textprops, labeldistance=1.2)  # Adjust label distance
        
        # Optional: Adjust font size specifically for the percentages
        for autotext in autotexts:
            autotext.set_fontsize(8)  # Adjust the font size of the percentages
        
        # Add a legend outside the pie chart
        ax.legend(wedges, filtered_categories, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Spending by Category', fontsize=14)  # Set the desired font size for the title
        plt.show()
    
    def create_line_graph(self):
        data = self.get_all_data()

        if not data:
            print("No available data")
            return
        
        #dataframe
        df = pd.DataFrame(data, columns = ['Date', 'Post_Date', 'Description', 'Category', 'Type', 'Amount', 'Memo'])
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        #group by month
        df['Month'] = df['Date'].dt.to_period('M') 

        df=df[df['Amount'] < 0]
        monthly_spending = df.groupby('Month')['Amount'].sum()

        monthly_spending = monthly_spending.abs()

        fig, ax = plt.subplots()
        monthly_spending.plot(ax=ax)

        ax.set_title('Spending Over Time')
        ax.set_xlabel('Month')
        ax.set_ylabel('Total Spending')

        plt.show()






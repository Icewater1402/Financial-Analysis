import sqlite3
import matplotlib.pyplot as plt

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






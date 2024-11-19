# Financial Analysis Project
* Personal Project 1

# Identifying Information
* Name: Christopher Isidro
* Email: chris.isidro18@gmail.com
* Collaborators: Christopher Isidro

# Source Files
* README.md
* main.py
* summarizer.py
* data_importer.py

# References
* GPT-3.5 Debugging and MatPlot Syntax 

# Known Errors
* This program accepts CSV files from Chase ONLY (for now)

# Build Instructions
* python3 main.py
* Select your CSV file from Chase

# How it Works
* Run the program 
* Select the CSV you would like to analyze
* Use the terminal to choose which information you would like to view
* Divide by month and categorize between paycheck, living expenses, gas, grocery, other

# Features
* Summary of each month (paychecks, total spending, ) [TOTAL SPENDING]
    * Total spending - essentials (calculated manually) = leisure

# What already exists
* Summary of Total Spendings (pie chart)


# What we want to add 
* Automated Sorting (export to excel file)
* How much money do I have for leisure per month? (adaptable monthly leisure cap)
* Per Month spendings (aside from complete) 
* Spending Predictions 
* Category Recommendations
* Anomaly Detection: Unusual Spending Patterns
* List by Category 

# CHANGELOG
## 07/05/2024
* Created repository
* Updated README 

## 07/15/2024
* Started Database with CSV import 
* Familiarized with queries and tables
* Research Pandas Python Library
* New Classes for functions for viewing summaries
* Organized functions into classes 
* Added tkinter library for windows explorer functionality and optimized pathfinding 

## 07/22/2024
* Implemented pie chart visual 
* Added new functions in summarizer.py
* Added .gitignore

## 09/22/2024
* Implemented Line Graph (trend over time)
* Added summarizer functions (summarize by category + list possible categories)

## 09/26/2024
* WHAT A NIGHTMARE
* I wanted to make a console class to make an interactive experience with importing and updating the database to visualize it better
* OH MAN the issue was that you run the console log while initializing the classes, but the classes normally got their file path in MAIN. So what happened was there was a shit ton of initialization errors 
* Was not able to make it work, so we'll try again another day ;) 
* Reverted back to what was working, I should totally make a branch next time 

## 09/30/2024
* Nightmare is over. Console is properly implemented in console.py
* Options work as intended. The frontend works properly
* New options include data import and export 
* Data import needs to be able to add onto existing databse (work in progress)
* Data export works as intended so far.  Multiple sheets of month summary and overall summary of simple averages and totals 
* Future updates include: Importing salaries, importing positive values, "money saved", and repeated billings 

## 10/11/2024
* Fixed issue with table not existing upon running code 
* Added essentials category where user can pick categories they want to list as essential 
* Issue with format of "snapshot" in excel export 
* Future idea: allow users to manually input income (as the program ignores all positive values) 

## 11/12/2024
* Checked to see if program works with bank statements instead of credit card 
* Columns are not identical between credit card and bank (for chase) 
* translations are going to be worked on in the future. For now, same credit statements :) 
* Small fix with sheet order on data export. Monthly summary now appears first before detailed transactions
* Updated exccel export formatting- more catered towards ateh 

## 11/13/2024
* Added values for monthly summaries 
* FIXME: Essentials are still an option in the program but remains a category in spreadsheet

## 11/18/2024
* list every unique transaction 
    * identify through console (bill/gas/recurring)
    * store as var/dict -> export to chase with matching names 
* FIXME: new column after amount
* FIXME: reformat excel to 1-1 ateh example 
* FIXME: get rid of essentials feature 
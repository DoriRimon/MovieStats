import csv
import os.path
import mysql.connector

# connection to server details

# my_sql_connector

# definitions on how to insert different data to DB

# retrieve data from API


# retrieve data form csv

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "static/data/filename.csv")
with open(path) as f:
    test = list(csv.reader(f))
    print(test)

# insert data to DB
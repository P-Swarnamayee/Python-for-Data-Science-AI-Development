import sqlite3
import pandas as pd

conn = sqlite3.connect("STAFF.db")

table_name = "INSTRUCTOR"
attribbute_list = ['ID','FNAME','LNAME','CITY','CCODE']

#reading the csvfile
file_path = "C:\PortfolioProjects\PortfolioProjects\Python_Project_For_DataEngineering\dirdb\INSTRUCTOR.csv"
df = pd.read_csv(file_path, names=attribbute_list)

#Loading the data to a table
df.to_sql(table_name, conn, if_exists = 'replace', index =False)
print('Table is ready')

#Python commands to run basic queries on the data
#1) Viewing all the data in the tbale
query_statement = f"SELECT * FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

#2) Viewing only FNAME column of data
query_statement = f"SELECT FNAME FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

#3) Viewing the total number of entries in table
query_statement = f"SELECT COUNT(*) FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

'''
Now try appending some data to the table. Consider the following.
a. Assume the ID is 100.
b. Assume the first name, FNAME, is John.
c. Assume the last name as LNAME, Doe.
d. Assume the city of residence, CITY is Paris.
e. Assume the country code, CCODE is FR.

'''
data_dict = { 'ID':[100],
            'FNAME':['John'],
            'LNAME':['Doe'],
            'CITY':['Paris'],
            'CCODE':['FR']
          }

data_append = pd.DataFrame(data_dict)

#To append INSTRUCTOR table:
data_append.to_sql(table_name,conn,if_exists='append',index=False)
print("Data appended successfully")

query_statement = f"SELECT COUNT(*) FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

#after execution, we can see an increase by 1 in the ouput for the first count query and the second one.

conn.close()
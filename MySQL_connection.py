""" Connect to MySQL database using user: python_pt """

import mysql.connector
from mysql.connector import errorcode

connection_args = {
  "host":"localhost", 
  "user":"python_pt", 
  "password":"1234"
  # database = "database_name"   # Connect to databse at login.
  }
  
def connect_to_mysql_server(args=connection_args):
  try:
    connection = mysql.connector.connect(**args)
    if connection.is_connected():
      print("Connected to server!")
      return connection
  except mysql.connector.Error as error:
    if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:   
      print(("Something is wrong with your user name or password"))
      raise ValueError from error
    elif error.errno == errorcode.ER_BAD_DB_ERROR:        
      print("Database does not exist")
      raise ValueError from error
  else:
    print("Closing connection from MySQL_connection.connect_to_mysql_server()")
    connection.close()

# print(mydb) # <mysql.connector.connection_cext.CMySQLConnection object at 0x0000012BA05D1D60> PS C:\Users\lconn\Documents\Programming\Python\Python Projects\Portuguese_Verb_Database> 

# print(connect_to_mysql_server())

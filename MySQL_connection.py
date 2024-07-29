""" Connect to MySQL server or database (if given) using user: python_pt password: 123. """

import mysql.connector
from mysql.connector import errorcode

connection_args = {
  "host":"localhost", 
  "user":"python_pt", 
  "password":"123",
  "database": None   # Connect to databse at login.
  }
  
def connect_to_mysql_server(args=connection_args):
  try:
    connection = mysql.connector.connect(**args)
    if connection.is_connected():
      return connection
  except mysql.connector.Error as error:
    print(f"ERROR CONNECTING TO SERVER\nDEBUG INFO\nError number: {error.errno}\nError message: {error.msg}")
    return None

  else:
    print("Closing connection from MySQL_connection.connect_to_mysql_server()")
    connection.close()
    return "Error occured"

# print(mydb) # <mysql.connector.connection_cext.CMySQLConnection object at 0x0000012BA05D1D60> PS C:\Users\lconn\Documents\Programming\Python\Python Projects\Portuguese_Verb_Database> 

# print(connect_to_mysql_server())

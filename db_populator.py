""" Enter this module if MySQL server conneciton made """
import mysql.connector
import MySQL_connection

class Database:
    def __init__(self, connection, data, db=None, create_new_db=True) -> None:
        self.connection = connection
        self.data = data
        self.db = db
        self.create_new_db = create_new_db

    def create_db(self):
        db_name = str(input("Enter the name of the database to create: "))
        create_database_query = f"CREATE DATABASE IF NOT EXISTS {db_name};"
        cursor = self.connection.cursor()
        cursor.execute(create_database_query)
        # Create 4 Tables
        # Longest Portuguese root veb: anticonstitucionalizar

    def store_row(self):
        pass
    
    def populate_db(self):
        if self.create_new_db:
            print("User wants to create new db.")
            self.create_db()
        else:
            # database does exist.  
            return False

    """ Use to check User Input """
    # def check_db_exists(self, db_name):
    #     cursor = self.conneciton.cursor()
    #     cursor.execute("SHOW DATABASES")
    #     databases = cursor.fetchall()
    #     if db_name in databases:
    #         return True
    #     return False

connection = MySQL_connection.connect_to_mysql_server()
x = Database(connection, data="", create_new_db=True)
print(x.populate_db())
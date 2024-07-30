""" Enter this module if MySQL server conneciton made """
import mysql.connector
import MySQL_connection
from scraper import Scraper

class Database:
    def __init__(self, connection, data, db_name=None, create_new_db=True) -> None:
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.data = data
        self.db_name = db_name
        self.create_new_db = create_new_db

    def create_db(self, db_name):
        create_database_query = f"CREATE DATABASE IF NOT EXISTS {db_name};"
        self.cursor.execute(create_database_query)
        self.cursor.execute(f"USE {db_name}")
        # Create 4 Tables
        # TODO: change VARCHAR(n) values.
        self.cursor.execute("""CREATE TABLE Verb(
                       id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
                       Verb VARCHAR(21) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci)
                       """)   # Longest Portuguese root veb: anticonstitucionalizar
        self.cursor.execute("""CREATE TABLE Tense(
                       id TINYINT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
                       Tense VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci)
                       """)
        self.cursor.execute("""CREATE TABLE Pronoun(
                       id TINYINT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
                       Pronoun VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci)
                       """)
        self.cursor.execute("""CREATE TABLE Conjugation(
                       id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
                       Verb INT UNSIGNED, 
                       Tense TINYINT UNSIGNED, 
                       Pronoun TINYINT UNSIGNED, 
                       Conjugation VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci, 
                       Irregular BOOLEAN,
                       FOREIGN KEY (Verb) REFERENCES Verb(id),
                       FOREIGN KEY (Tense) REFERENCES Tense(id),
                       FOREIGN KEY (Pronoun) REFERENCES Pronoun(id))
                       """)
        # TODO: populate these tables.
        # if error, close connection.
        # Close the cursor, close the connection


    def store_row(self, data):
        for verb in data:
            for tense in data[verb]:
                for row in data[verb][tense]:
                    pronoun, conjugation, irregular = row
                    # If pronoun is right for the tense

                    # TODO: retrieve id's one by one for error catching.
                    VALUES = f""" (SELECT id FROM Verb WHERE Verb = '{verb}'),
                    (SELECT id FROM Tense WHERE Tense = '{tense}'),
                    (SELECT id FROM Pronoun WHERE Pronoun = '{pronoun}'),
                    '{conjugation}',
                    {irregular}
                    """
                    # else return None
                    self.cursor.execute(f"INSERT INTO conjugation (Verb, Tense, Pronoun, Conjugation, Irregular), {VALUES}")
    
    def populate_db(self, data):
        if self.create_new_db:
            print("User wants to create new db.")
            self.db_name = str(input("Enter the name of the database to create: "))
            self.create_db(self.db_name)
        
        # for verb in data:
        #     for tense in verb:
        #         pronoun, conjugation, irregular = data[verb][tense]
        #         print(pronoun, conjugation, irregular)
        for tense in data:
            for t in data[tense]:
                print(t)
                pronoun, conjugation, irregular = t
                print(pronoun, conjugation, irregular)
            

# connection = MySQL_connection.connect_to_mysql_server()
x = Database(connection="", data="", create_new_db=False)
# print(x.populate_db())


# y = Scraper("https://conjugator.reverso.net/conjugation-portuguese-verb-poder.html")
# data = y.parse()
# x.populate_db(data=data)

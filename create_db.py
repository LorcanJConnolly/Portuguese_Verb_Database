import mysql.connector
from dataset_structure import structure_dict

def create_db(self, db_name, connection):
        """ 
        Initialise the database db_name and its 4 tables.
        Verb: An ID table for each verb stored in the database.
        Pronoun: An ID table for each prounoun a conjugation is stored under in the database.
        Tense: An ID table for each tense a conjugation is stored under in the database.
        Conjugation: A Table containing conjugations and their corresponding Verb ID, Tense ID, Pronoun ID, and a boolean Irregular value.
        """
        cursor = connection.cursor()

        try:
            create_database_query = f"CREATE DATABASE IF NOT EXISTS {db_name};"
            self.cursor.execute(create_database_query)
            self.cursor.execute(f"USE {db_name}")
            self.cursor.execute("""CREATE TABLE Verb(
                        id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
                        Verb VARCHAR(21) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci UNIQUE)
                        """)   # Longest Portuguese root veb: anticonstitucionalizar
            self.connection.commit()
            self.cursor.execute("""CREATE TABLE Tense(
                        id TINYINT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
                        Tense VARCHAR(63) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci UNIQUE)
                        """)
            self.connection.commit()
            self.cursor.execute("""CREATE TABLE Pronoun(
                        id TINYINT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
                        Pronoun VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci UNIQUE)
                        """)
            self.connection.commit()
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
            self.connection.commit()
            self.cursor.execute("INSERT IGNORE INTO Pronoun (Pronoun) VALUES (NULL)")   # Insert a Null ID reference for conguations without pronouns.

            """ Populated Key Tables. """
            for tense, pronouns in structure_dict.items():
                self.cursor.execute("INSERT INTO Tense (Tense) VALUES (%s)", (tense,))
                self.connection.commit()
                if pronouns is not None:
                    for pronoun in pronouns:
                        self.cursor.execute("INSERT IGNORE INTO Pronoun (Pronoun) VALUES (%s)", (pronoun,))   # Ignore duplicates.
                        self.connection.commit()
                        
        except mysql.connector.Error as error:
            print(f"ERROR CREATING DATABASE\nDEBUG INFO\nError number: {error.errno}\nError message: {error.msg}")
            self.cursor.execute(f"DROP DATABASE {db_name}")
            # FIXME: can drop database because we check the user input db_name doesn't exist at input.
    
import mysql.connector
from dataset_structure import structure_dict

def create_db(db_name, connection):
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
            cursor.execute(create_database_query)
            cursor.execute(f"USE {db_name}")
            cursor.execute("""CREATE TABLE Verb(
                        id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
                        Verb VARCHAR(21) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci UNIQUE)
                        """)   # Longest Portuguese root veb: anticonstitucionalizar
            connection.commit()
            cursor.execute("""CREATE TABLE Tense(
                        id TINYINT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
                        Tense VARCHAR(63) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci UNIQUE)
                        """)
            connection.commit()
            cursor.execute("""CREATE TABLE Pronoun(
                        id TINYINT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
                        Pronoun VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci UNIQUE)
                        """)
            connection.commit()
            cursor.execute("""CREATE TABLE Conjugation(
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
            connection.commit()
            cursor.execute("INSERT IGNORE INTO Pronoun (Pronoun) VALUES (NULL)")   # Insert a Null ID reference for conguations without pronouns.

            """ Populated Key Tables. """
            for tense, pronouns in structure_dict.items():
                cursor.execute("INSERT INTO Tense (Tense) VALUES (%s)", (tense,))
                connection.commit()
                if pronouns is not None:
                    for pronoun in pronouns:
                        cursor.execute("INSERT IGNORE INTO Pronoun (Pronoun) VALUES (%s)", (pronoun,))   # Ignore duplicates.
                        connection.commit()

        except mysql.connector.Error as error:
            print(f"ERROR CREATING DATABASE\nDEBUG INFO\nError number: {error.errno}\nError message: {error.msg}")
            # if it exists in the database
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
    
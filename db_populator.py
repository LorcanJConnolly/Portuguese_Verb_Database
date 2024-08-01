""" Enter this module if MySQL server conneciton made """
import mysql.connector
import MySQL_connection
from scraper import Scraper
from dataset_structure import structure_dict

class Database:
    def __init__(self, connection, db_name=None, create_new_db=True) -> None:
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.db_name = db_name
        self.create_new_db = create_new_db

    def create_db(self, db_name):
        """ 
        Initialise the database db_name and its 4 tables.
        Verb: An ID table for each verb stored in the database.
        Pronoun: An ID table for each prounoun a conjugation is stored under in the database.
        Tense: An ID table for each tense a conjugation is stored under in the database.
        Conjugation: A Table containing conjugations and their corresponding Verb ID, Tense ID, Pronoun ID, and a boolean Irregular value.
        """
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
            print(f"ERROR CREATING DATABASE\nDEBUG INFO\nError number: {error.errno}\nError message: {error.msg}\nDATABASE MAY REQUIRE DROPPING.")
            # FIXME: can drop database because we check the user input db_name doesn't exist at input.
    
    def store_verb(self, verb):
        self.cursor.execute(f"USE {self.db_name}")
        # Insert the root Verb into Verb table to generated a Primary Key.
        self.cursor.execute("INSERT IGNORE INTO Verb (Verb) VALUES (%s)", (verb,))
        self.connection.commit()

    def store_row(self, verb, tense, pronoun, conjugation, irregular):
        """
        Stores the given pronoun, conjugation, and irregular value in the database.
        """
        print("INSERTING ROW:", verb, tense, pronoun, conjugation, irregular)
        self.cursor.execute(f"USE {self.db_name}")

        self.cursor.execute("SELECT id FROM Verb WHERE Verb = %s", (verb,))
        verb_id = self.cursor.fetchone()
        if verb_id is None:
            raise ValueError(f"Pronoun '{verb}' does not exist in the Pronoun table")
        verb_id = verb_id[0]

        self.cursor.execute("SELECT id FROM Pronoun WHERE Pronoun = %s", (pronoun,))
        pronoun_id = self.cursor.fetchone()
        if pronoun_id is None:
            raise ValueError(f"Pronoun '{pronoun}' does not exist in the Pronoun table")
        pronoun_id = pronoun_id[0]

        self.cursor.execute("SELECT id FROM Tense WHERE Tense = %s", (tense,))
        tense_id = self.cursor.fetchone()
        if tense_id is None:
            raise ValueError(f"Tense '{tense}' does not exist in the Tense table")
        tense_id = tense_id[0]
        
        self.cursor.execute("INSERT INTO Conjugation (Verb, Tense, Pronoun, Conjugation, Irregular) VALUES (%s, %s, %s, %s, %s)", (verb_id, tense_id, pronoun_id, conjugation, irregular))
        self.connection.commit()
        

    def populate_db(self, dataset):
        if self.create_new_db:
            # TODO: Move this to input
            print("User wants to create new db.")
            self.db_name = str(input("Enter the name of the database to create: "))
            self.create_db(self.db_name)
            print("Database created")

        errors = {}   # Dictionary contains {Verb that triggered error : Error reason}.
        for verb in dataset:
            error_occured = False
            for tense in dataset[verb]:
                if tense not in structure_dict:
                    errors[verb] = f"ERROR: Extracted tense: {tense} is not recognised."
                    error_occured = True
                    break
                expected_pronouns = structure_dict[tense]
                for values, expected_pronoun in zip(dataset[verb][tense], expected_pronouns):
                    if len(values) != 3:
                        errors[verb] = f"ERROR: {values} does not contain a pronoun, comjugation, and iregular type."
                        error_occured = True
                        break
                    pronoun, conjugation, irregular = values
                    if pronoun is None: pronoun = "NULL"
                    if len(dataset[verb][tense]) != len(expected_pronouns):
                        errors[verb] = f"ERROR: expected {len(expected_pronouns)} pronouns: {expected_pronouns} in tesnse: {tense} but only got {len(dataset[verb][tense])} in {dataset[verb][tense]}"
                        error_occured = True
                        break
                    if expected_pronoun != pronoun:
                        errors[verb] = f"ERROR: expected pronoun '{expected_pronoun}' != given pronoun '{pronoun}' in tesnse: {tense}."
                        error_occured = True
                        break
                    else:
                        # TODO: check if verb is duplicate
                        self.store_verb(verb)
                        self.store_row(verb, tense, pronoun, conjugation, irregular)
                if error_occured:
                    break
            if error_occured:
                """ Skip the entire verb dataset for a verb that raises an error. """
                continue
        if errors:
            print(f"The following verbs were extracted incorrectly and could not be stored in the databse: \n{errors}")
    
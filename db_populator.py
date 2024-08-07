""" Inserts a verb dataset into the database. Can also initialise the database if required. """
import mysql.connector
import MySQL_connection
from scraper import Scraper
from dataset_structure import structure_dict

class Database:
    def __init__(self, connection, verb, db_name) -> None:
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.verb = verb
        self.db_name = db_name

    def store_verb(self, verb):
        """
        Stores a new root verb into the Verb table to generate its key.
        """
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
            raise ValueError(f"Verb '{verb}' does not exist in the Pronoun table")
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
        
    def populate_db(self, dataset, verb):
        """
        Iterates over the dataset and compares the structure and data to the expected values using structure_dict from dataset_structure.
        """
        errors = {}   # Dictionary contains {Verb that triggered error : Error reason}.
        # TODO: test the new added error raising
        # TODO: test that this inputs a single verb correctly
        try:
            for tense in dataset[verb]:
                if tense not in structure_dict:
                    errors[verb] = f"ERROR: Extracted tense: {tense} is not recognised."
                    raise ValueError
                expected_pronouns = structure_dict[tense]
                for values, expected_pronoun in zip(dataset[verb][tense], expected_pronouns):
                    if len(values) != 3:
                        errors[verb] = f"ERROR: {values} does not contain a pronoun, comjugation, and iregular type."
                        raise ValueError
                    pronoun, conjugation, irregular = values
                    if pronoun is None: pronoun = "NULL"
                    if len(dataset[verb][tense]) != len(expected_pronouns):
                        errors[verb] = f"ERROR: expected {len(expected_pronouns)} pronouns: {expected_pronouns} in tesnse: {tense} but only got {len(dataset[verb][tense])} in {dataset[verb][tense]}"
                        raise ValueError
                    if expected_pronoun != pronoun:
                        errors[verb] = f"ERROR: expected pronoun '{expected_pronoun}' != given pronoun '{pronoun}' in tesnse: {tense}."
                        raise ValueError
                    else:
                        self.store_verb(verb)
                        self.store_row(verb, tense, pronoun, conjugation, irregular)
        except Exception as e:
            print("Errors:", errors)
            print("Exception:", str(e))
            
    
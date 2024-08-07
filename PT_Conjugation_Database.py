# UI
#   Create an excel extractor
#   Test inputs (multiple of the same verb).
from scraper import Scraper
from db_populator import Database
from create_db import create_db
import MySQL_connection

"""Create a delay between requests."""
import time
import random

import argparse
import os
import re

"""
self.connection = MySQL_connection.connect_to_mysql_server()
        self.cursor = self.connection.cursor()
        self.test_db_name = "test_db_populator_create_db"
    
        self.cursor.execute("SHOW DATABASES")
        databases = [database[0] for database in self.cursor.fetchall()]
        if self.test_db_name in databases:
            raise Exception(f"ERROR: Database '{self.test_db_name}' already exists. Aborting tests to prevent accidental data loss.")
"""

def input_type(input):
    if os.path.isfile(input) and os.path.splitext(input)[1] == ".xlsx" or os.path.splitext(input)[1] == ".xls":
        # extract from excel.
        # return verbs
        pass
    else:
        return [verb.strip() for verb in input.split()]

# FIXME: requires two inputs, how do we get this from args
def validate_db_name(name, create_new_databse):
    """ Checks if given database name contains the correct characters for a MySQL database. """
    if re.match(r'^[A-Za-z0-9_]+$', name):
        if is_unique_name(name, create_new_databse):
            return name
        else:
            raise ValueError(is_unique_name(name, create_new_databse))
    else:
        raise argparse.ArgumentTypeError("Invalid database name. Must contain only alphanumeric characters and underscores, with no spaces.")

# FIXME: requires two inputs, how do we get this from args
def is_unique_name(name, create_new_databse):
    """ 
    If creating a new database, checks if given database name already exists in the database. 
    If creating adding to an existing database, checks if given database name already exists in the database. 
    """
    connection = MySQL_connection.connect_to_mysql_server()
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES")
    databases = [database[0] for database in cursor.fetchall()]
    cursor.close()
    connection.close()
    if name in databases and create_new_databse == "Y":
        return f"Database name: '{name}' already exists in the database. Please choose another name."
    if name not in databases and create_new_databse == "N":
        return f"Database name: '{name}' does not exist in the database. Please choose another name from: {databases}."
    return True

def exist_in_database(connection, verb):
    """ Checks if a verb exists in the database already. """
    cursor = connection.cursor()
    cursor.execute(f"USE {args.database_name}")
    cursor.execute("SELECT id FROM Verb WHERE Verb = %s", (verb,))
    verb_id = cursor.fetchone()
    cursor.close()
    if verb_id is None:
        return False
    else:
        return True


if __name__ == '__main__':
    """
    
    """
    print(validate_db_name("test", "Y"))
    # python [file.py] [verbs] [database name] [create new database] // [JSON file name] [Create new JSON file]
    parser = argparse.ArgumentParser(description="Scrape verb webpage(s) and insert data into a MySQL database.")
    parser.add_argument("verbs", type=input_type, help="Input the verb(s) with a whitespace delimiter or the directory of an excel file containing only a list of verbs.")   # args.verbs
    parser.add_argument("database_name", help="The name of the database to populate. Must exist in databse if create_database is set to 'N'.")
    parser.add_argument("create_new_databse", choices=['Y', 'N'], help="Y/N.\n'Y': create a new database with the name: [database_name].\n'N': add to an existing database with the name: [database_name].")
    args = parser.parse_args()
    
    try:
        validate_db_name(args.database_name, args.create_new_databse)
    except Exception as e:
        print(e)

    print(args)

    connection = MySQL_connection.connect_to_mysql_server() 
    if args.create_new_databse == "Y":
        create_db(args.database_name, connection)
    
    dataset = {}

    for verb in args.verbs: 
        if not exist_in_database(connection, verb):
            print("Scraping the verb: ", verb)
            url = f"https://conjugator.reverso.net/conjugation-portuguese-verb-{verb}.html"
            time.sleep(random.uniform(10, 20))
            scraper = Scraper(url=url, verb=verb, global_dataset=dataset)
            # Insert the verb into database
            populator = Database(connection=connection, db_name=args.database_name, verb=verb)
            populator.populate_db(dataset, verb)
            dataset = scraper.parse()
        else:
            print(f"Skpping the verb: '{verb}' as it already exists in the database.")

    # Once done we extract to JSON file.




    

 



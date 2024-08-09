# UI
#   Create an excel extractor
#   Test inputs (multiple of the same verb).
from scraper import Scraper
from db_populator import Database
from create_db import create_db
import MySQL_connection
import excel_to_list

import time
import random

import argparse
import os
import re
from string import punctuation

# TODO: Add a way of removing a verb and its data from the database incase of wrong entry.

def input_type(input):
    """ Checks if Verbs are manually inputted as a list or are to be extracted from an Excel spreadsheet. """
    if os.path.isfile(input) and os.path.splitext(input)[1] == ".xlsx" or os.path.splitext(input)[1] == ".xls":
        return excel_to_list.extract()
    else:
        return input
        #FIXME output cant be a list
        # return [verb.strip().strip(punctuation).lower() for verb in input.split()]

def validate_db_name(name, create_new_databse):
    """ Checks if given database name contains the correct characters for a MySQL database. """
    if re.match(r'^[A-Za-z0-9_]+$', name):
        if is_unique_name(name, create_new_databse):
            return name
        else:
            raise ValueError(is_unique_name(name, create_new_databse))
    else:
        raise argparse.ArgumentTypeError(f"\nERROR: Invalid database name '{name}'.\n   Database name must contain only alphanumeric characters and underscores, with no spaces.\n")

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
    if name in databases and create_new_databse == "y":
        raise ValueError(f"\nERROR: Database name: '{name}' already exists in the database.\n   Please choose another name NOT from: {databases}.\n")
    if name not in databases and create_new_databse == "n":
        raise ValueError(f"\nERROR: Database name: '{name}' does not exist in the database.\n   Please choose another name from: {databases}.\n")
    return True

def exist_in_database(connection, verb, db_name):
    """ Checks if a verb exists in the database already. """
    cursor = connection.cursor()
    cursor.execute(f"USE {db_name}")
    cursor.execute("SELECT id FROM Verb WHERE Verb = %s", (verb,))
    verb_id = cursor.fetchone()
    cursor.close()
    if verb_id is None:
        return False
    else:
        return True



if __name__ == '__main__':
    """
    CLI inputs.
    """
    # python [file.py] [verbs] [database name] [create new database] // [JSON file name] [Create new JSON file]
    parser = argparse.ArgumentParser(description="Scrape verb webpage(s) and insert data into a MySQL database.")
    parser.add_argument("verbs", type=input_type, nargs='+', help="Input the verb(s) with a whitespace delimiter or the directory of an excel file containing only a list of verbs.")   # args.verbs
    parser.add_argument("database_name", help="The name of the database to populate. Must exist in databse if create_database is set to 'N'.")
    parser.add_argument("create_new_databse", choices=['Y', 'N', 'y', 'n'], help="Y/N.\n'Y': create a new database with the name: [database_name].\n'N': add to an existing database with the name: [database_name].")
    args = parser.parse_args()
    
    try:
        validate_db_name(args.database_name, args.create_new_databse.lower())
    except Exception as e:
        print(e)

    connection = MySQL_connection.connect_to_mysql_server() 

    if args.create_new_databse.lower() == "y":
        create_db(args.database_name, connection)
    
    dataset = {}
    print("args.verb: ", args.verbs)
    for verb in args.verbs: 
        print("verb: ", verb)
        if not exist_in_database(connection, verb, args.database_name):
            print("Scraping the verb: ", verb)
            url = f"https://conjugator.reverso.net/conjugation-portuguese-verb-{verb}.html"
            time.sleep(random.uniform(10, 20))
            scraper = Scraper(url=url, verb=verb, global_dataset=dataset)
            dataset = scraper.parse()
            print("Scraping complete.")
            # Insert the verb into database
            populator = Database(connection=connection, db_name=args.database_name, verb=verb, global_dataset=dataset)
            populator.populate_db(dataset, verb)
        else:
            print(f"\nERROR: Verb exists in database. \n  Skpping the verb: '{verb}'.\n")

    # Once done we extract to JSON file.




    

 



# UI
from scraper import Scraper
from db_populator import Database
import MySQL_connection

"""Create a delay between requests."""
import time
import random

"""
self.connection = MySQL_connection.connect_to_mysql_server()
        self.cursor = self.connection.cursor()
        self.test_db_name = "test_db_populator_create_db"
    
        self.cursor.execute("SHOW DATABASES")
        databases = [database[0] for database in self.cursor.fetchall()]
        if self.test_db_name in databases:
            raise Exception(f"ERROR: Database '{self.test_db_name}' already exists. Aborting tests to prevent accidental data loss.")
"""


if __name__ == '__main__':
    # Give input verbs
    verbs = ["acabar", "acalmar", "achar", "advinhar", "adorar", "ajudar", "almoçar", "amar", "analisar", "andar", "aniquilar", "apressar", "arrotar", "barbear", "bocejar", "buscar"]
    dataset = {}
    for verb in verbs:
        print("Scraping ", verb)
        url = f"https://conjugator.reverso.net/conjugation-portuguese-verb-{verb}.html"
        # def __init__(self, url, verb, global_dataset) -> None:
        delay = random.uniform(15,25)
        time.sleep(delay)
        scraper = Scraper(url=url, verb=verb, global_dataset=dataset)
        dataset = scraper.parse()
    for v in dataset:
        print(v)

    # Please provid a database name or type NEWDATABASE to create a new database.
    input_name = "NEWDATABASE"
    input_create = False
    if input_name == "NEWDATABASE":
        # Give name of new db
        input_name = "test_new"
        input_create = True
    
    print("adding to db")
    connection = MySQL_connection.connect_to_mysql_server()
    # def __init__(self, connection, dataset, db_name=None, create_new_db=True) -> None:
    populator = Database(connection=connection, db_name=input_name, create_new_db=input_create)
    populator.populate_db(dataset=dataset)
    


# get db 
# if new -> get name -> check if there's any conflict.
# if not -> get db

# get dataset from scraper
# populate db using db_populator

# close connection and cursor.


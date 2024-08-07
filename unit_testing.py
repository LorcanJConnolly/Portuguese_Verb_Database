import unittest
from bs4 import BeautifulSoup
from mysql.connector import errorcode
from scraper import Scraper
from sample_html import html_dict
from db_populator import Database
import MySQL_connection
import create_db
from sample_dataset import dataset_dict
import PT_Conjugation_Database
import argparse

# FIXME: create_db moved to create_db.py
# TODO: Test that create_db error raised actually drops the database.

class TestHtmlExtraction(unittest.TestCase):
    """
    Tests relating to the html extraction in Sraper.get_html.
    """
    def setUp(self) -> None:
        """
        Initialise Scraper object for each test.
        """
        self.obj = Scraper(url="", verb="", global_dataset={})

    def test_missing_url(self):
        """
        Test that an invalid or non-functioning url returns None.
        """
        missing_url = "123"
        self.assertIsNone(self.obj.get_html(missing_url))

    def test_sample_url(self):
        """
        Test that a valid url from another webnsite returns a BeautifulSoup Object.
        """
        sample_url = "https://docs.scrapy.org/en/latest/_static/selectors-sample1.html"
        self.assertIsInstance(self.obj.get_html(sample_url), BeautifulSoup)

    def test_target_url(self):
        """
        Test that a valid url from Reverso returns a BeautifulSoup Object.
        """
        target_url = "https://conjugator.reverso.net/conjugation-portuguese-verb-ter.html"
        self.assertIsInstance(self.obj.get_html(target_url), BeautifulSoup)

    def test_error_raised(self):    
        """
        Test that checks correct Error is raised for missing url.
        """
        self.obj.url = "123"
        with self.assertRaises(ValueError): 
            self.obj.parse()

    def test_response_error_4XX(self):
        """
        Tests to see if 4XX client errors are caught when fetching a response from url.
        """
        error_codes = [400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 421, 422, 423, 424, 425, 426, 428, 429, 431, 451]
        for error_code in error_codes:
            url = f"https://httpbin.org/status/{error_code}"
            self.assertIsNone(self.obj.get_html(url))

    def test_response_error_5XX(self):
        """
        Tests to see if 5XX server errors are caught when fetching a response from url.
        """
        error_codes = [500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511]
        for error_code in error_codes:
            print(error_code)
            url = f"https://httpbin.org/status/{error_code}"
            self.assertIsNone(self.obj.get_html(url))
        
class TestTextExtractionFromTags(unittest.TestCase):
    """
    Test relating to text extraction from fetched html using Scraper.extract_text_from_tags.
    """
    # FIXME: Test documentation.
    # FIXME: Add verb layer.
    def setUp(self) -> None:
        """
        The Verb used for testing is ter.
        """
        self.obj = Scraper("", verb='ter', global_dataset={})
    
    def test_tense_only_extraction(self):
        """
        Test for extracting the Tense from a tag.
        """
        soup = BeautifulSoup(html_dict['html_tense'], 'html.parser')
        # self.assertEqual(self.obj.extract_text_from_tags(soup), {'ter':{'Indicativo Presente': []}})
        self.assertEqual(self.obj.extract_text_from_tags(soup), {'ter': {'Indicativo Presente': []}})

    def test_tense_pronoun_conjugation_extraction(self):
         """ 
         Test for extracting the Tense, Pronoun, Conjugation, and Iregular value from a tag.
         """
         soup = BeautifulSoup(html_dict['html_tense_pronoun_conjugation'], 'html.parser')
         self.assertEqual(self.obj.extract_text_from_tags(soup), {'ter':{'Indicativo Presente': [('eu', 'tenho', True)]}})

    def test_tense_aux_pronoun_conjugation_extraction(self):
         """ 
         Test for extracting the Tense, Auxiliary Proun + Pronoun, Conjugation, and Iregular value from a tag.
         """
         soup = BeautifulSoup(html_dict["html_tense_aux_pronoun_conjugation"], 'html.parser')
         self.assertEqual(self.obj.extract_text_from_tags(soup), {'ter':{'Indicativo Pretérito Perfeito Composto': [('eu tenho', 'tido', False)]}})

    def test_wrong_class(self):
         """ 
         Test for no extraction from wrong tags.
         """
         soup = BeautifulSoup(html_dict["html_wrong_class"], 'html.parser')
         self.assertEqual(self.obj.extract_text_from_tags(soup), {'ter':{}})

    def test_multiple_tags_extraction(self):
         """ 
         Test for extracting the Tense, Auxiliary Proun + Pronoun, Conjugation, and Iregular value from multiple tags.
         """
         soup = BeautifulSoup(html_dict["html_multiple_tags"], 'html.parser')
         self.assertEqual(self.obj.extract_text_from_tags(soup), {'ter':{'Condicional Futuro do Pretérito Simples': [('eu', 'teria', False), ('tu', 'terias', False), ('ele/ela/você', 'teria', False), ('nós', 'teríamos', False), ('vós', 'teríeis', False), ('eles/elas/vocês', 'teriam', False)]}})
    
    def test_multiple_tags_tense_only_extraction(self):
         """ 
         Test for case of extracting from multiple tags contains on a Tense.
         """
         soup = BeautifulSoup(html_dict["html_multiple_tags_tense_only"], 'html.parser')
         self.assertEqual(self.obj.extract_text_from_tags(soup), {'ter':{'Gerúndio': [(None, 'tendo', False)], 'Particípio': [(None, 'tido', False)]}})

    def test_multiple_tags_tense_missing_extraction(self):
         """ 
          Test for no extraction from many wrong tags.
         """
         soup = BeautifulSoup(html_dict["html_multiple_tags_missing_tense"], 'html.parser')
         with self.assertRaises(KeyError):
             self.obj.extract_text_from_tags(soup)

class TestDatabaseConnection(unittest.TestCase):
    """
    Test to see if connection is formed to MySQL server using MySQL_connection.connect_to_mysql_server
    """
    def setUp(self):
        """
        Open a connection.
        """
        self.connection = None
        self.test_db_name = "test_db_populator_create_db"
        self.created_test_db = False

    def tearDown(self):
        """
        Close the connection.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def test_server_connection_success(self):
        """ 
        Tests if correct log-in results in a successful conneciton to the MySQL server. 
        """
        connection_args = {
            "host":"localhost", 
            "user":"python_pt", 
            "password":"123"
            }
        self.connection = MySQL_connection.connect_to_mysql_server(connection_args)
        self.assertIsNotNone(self.connection)

    def test_server_connection_failure(self):
        """ 
        Tests if incorrect log-in results in a successful conneciton to the MySQL server. 
        """
        connection_args = {
            "host":"localhost", 
            "user":"not_user", 
            "password":"wrong_password"
            }
        self.connection = MySQL_connection.connect_to_mysql_server(connection_args)
        self.assertIsNone(self.connection)

class TestDatabaseInteracitons(unittest.TestCase):
    # FIXME: all failing due to self.cursor = self.connection.cursor() being None
    """
    Test for storage in the chosen MySQL database using dp_populator.populate_db.
    """
    def setUp(self):
        """
        Create a test database that does not share a name with an already existing database.
        """
        self.connection = MySQL_connection.connect_to_mysql_server()
        if self.connection is not None:
            self.cursor = self.connection.cursor()
            self.test_db_name = "test_db_populator_create_db"
            self.cursor.execute("SHOW DATABASES")
            databases = [database[0] for database in self.cursor.fetchall()]
            if self.test_db_name in databases:
                raise Exception(f"ERROR: Database '{self.test_db_name}' already exists. Aborting tests to prevent accidental data loss.")
            create_db.create_db(db_name=self.test_db_name, connection=self.connection)
        else:
            raise "Error connecting to MySQL server with MySQL_connection.connect_to_mysql_server()."
   
    def tearDown(self):
        """
        Delete the test database.
        """
        self.cursor.execute(f"DROP DATABASE IF EXISTS {self.test_db_name}")
        self.cursor.close()
        self.connection.close()

    def test_database_created(self):
        """ 
        Tests if database is created 
        """
        self.cursor.execute("SHOW DATABASES")
        databases = [database[0] for database in self.cursor.fetchall()]
        self.assertIn(self.test_db_name, databases)

    def test_database_populated(self):
        """ 
        Tests if database is created and populated with tables. 
        """
        self.cursor.execute(f"USE {self.test_db_name}")
        self.cursor.execute("SHOW TABLES")
        tables = [table[0] for table in self.cursor.fetchall()]
        self.assertIn("verb", tables)
        self.assertIn("pronoun", tables)
        self.assertIn("tense", tables)
        self.assertIn("conjugation", tables)
        #TODO: Test tables are populated
    
    def test_database_idtables_populated(self):
        """
        Tests if database is created and ID tables are populated.
        """
        # TODO
        pass
    
    def test_create_db_is_unique_name(self):
         """
        Test to see if error is raised when requesting to create a new database with an input database name that already exists in the server.
        """
         with self.assertRaises(ValueError):
                PT_Conjugation_Database.is_unique_name(self.test_db_name, create_new_databse="Y")

    def test_add_to_existing_db_is_unique_name(self):
        """
        Test to see if error is raised when requesting to add to an existing database with an input database name that does not exist in the server.
        """
        doesnt_exist_test_db_name="This_name_doesnt_exist"
        self.cursor.execute("SHOW DATABASES")
        databases = [database[0] for database in self.cursor.fetchall()]
        if doesnt_exist_test_db_name in databases:
            raise Exception(f"ERROR: Database '{doesnt_exist_test_db_name}' exists so test will fail. Please change the test name: '{doesnt_exist_test_db_name}' to fix this test.")
        with self.assertRaises(ValueError):
            PT_Conjugation_Database.is_unique_name(doesnt_exist_test_db_name, create_new_databse="N")

        

    def test_single_row_insertion(self):
        """
        A test to see if data is correctly accepted and stored in the appropriate tables. 
        """
        # #FIXME: create Database object.
        # dataset = dataset_dict["single_verb"]
        # self.obj.dataset = dataset
        # # print(self.obj.data)
        # self.obj.store_row(data=self.obj.data)
        # # TODO: populate these tables.
        # # self.cursor.execute("SELECT * FROM verb")
        # # self.cursor.execute("SELECT * FROM pronoun")
        # # self.cursor.execute("SELECT * FROM tense")
        # self.cursor.execute("SELECT * FROM conjugation")
        # rows = [row for row in self.cursor.fetchall()]
        # print("rows: ", rows)
        # TODO
        pass

class TestMain(unittest.TestCase):
    def test_verb_input(self):
        input = "Poder"
        self.assertEqual(PT_Conjugation_Database.input_type(input), ["poder"])
        input = "Poder,"
        self.assertEqual(PT_Conjugation_Database.input_type(input), ["poder"])
        input = "PODER"
        self.assertEqual(PT_Conjugation_Database.input_type(input), ["poder"])
        
    def test_verbs_input(self):
        input = "Estar, Ser, Ter, Fazer, Ver, Vir"
        self.assertEqual(PT_Conjugation_Database.input_type(input), ["estar", "ser", "ter", "fazer", "ver", "vir"])
        input = "Estar Ser Ter Fazer Ver Vir"
        self.assertEqual(PT_Conjugation_Database.input_type(input), ["estar", "ser", "ter", "fazer", "ver", "vir"])
        input = "ESTAR, SER, TER, FAZER, VER, VIR"
        self.assertEqual(PT_Conjugation_Database.input_type(input), ["estar", "ser", "ter", "fazer", "ver", "vir"])

    def test_valid_db_name(self):
        """
        A test for valid database name inputs.
        """
        self.assertEqual(PT_Conjugation_Database.validate_db_name("A_valid_db_name", ""), "A_valid_db_name")
        self.assertEqual(PT_Conjugation_Database.validate_db_name("underscores_allowed", ""), "underscores_allowed")
        self.assertEqual(PT_Conjugation_Database.validate_db_name("numb3rs4ll0w3d", ""), "numb3rs4ll0w3d")
        
    def test_invalid_db_name(self):
        """
        A test for raising the correct error for invalid database name inputs.
        """
        with self.assertRaises(argparse.ArgumentTypeError):
            PT_Conjugation_Database.validate_db_name("----", "")
        with self.assertRaises(argparse.ArgumentTypeError):
            PT_Conjugation_Database.validate_db_name("wrong!!!", "")
        with self.assertRaises(argparse.ArgumentTypeError):
            PT_Conjugation_Database.validate_db_name(" ", "")    
        with self.assertRaises(argparse.ArgumentTypeError):
            PT_Conjugation_Database.validate_db_name("no spaces allowed ", "")    
        
if __name__ == '__main__':
    unittest.main()


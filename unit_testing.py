import unittest
from bs4 import BeautifulSoup
from mysql.connector import errorcode

from scraper import Scraper
from sample_html import html_dict
from db_populator import Database
import MySQL_connection
from sample_dataset import dataset_dict

class TestHtmlExtraction(unittest.TestCase):

    def test_missing_url(self):
        """Test that an invalid or non-functioning url returns None."""
        missing_url = Scraper(url="123", verb="", global_dataset={})
        self.assertIsNone(missing_url.get_html())

    def test_sample_url(self):
        """Test that a valid url from another webnsite returns a BeautifulSoup Object."""
        sample_url = Scraper(url="https://docs.scrapy.org/en/latest/_static/selectors-sample1.html", verb="", global_dataset={})
        self.assertIsInstance(sample_url.get_html(), BeautifulSoup)

    def test_target_url(self):
        """Test that a valid url from Reverso returns a BeautifulSoup Object."""
        target_url = Scraper(url="https://conjugator.reverso.net/conjugation-portuguese-verb-ter.html", verb="", global_dataset={})
        self.assertIsInstance(target_url.get_html(), BeautifulSoup)

    def test_error_raised(self):    
        """Test that checks correct Error is raised for missing url."""
        missing_url = Scraper("123", verb="", global_dataset={})
        with self.assertRaises(ValueError): 
            missing_url.parse()
        
class TestTextExtractionFromTags(unittest.TestCase):
    # FIXME: Test documentation.
    # FIXME: Add verb layer.
    def setUp(self) -> None:
        """Verb used for testing is ter."""
        self.obj = Scraper("", verb="ter", global_dataset={})
    
    def test_tense_only_extraction(self):
        """Test for extracting the tense from a tag."""
        soup = BeautifulSoup(html_dict["html_tense"], 'html.parser')
        # self.assertEqual(self.obj.extract_text_from_tags(soup), {'ter':{'Indicativo Presente': []}})
        self.assertEqual(self.obj.extract_text_from_tags(soup), {'ter': {'Indicativo Presente': []}})

    def test_tense_pronoun_conjugation_extraction(self):
         """ """
         soup = BeautifulSoup(html_dict["html_tense_pronoun_conjugation"], 'html.parser')
         self.assertEqual(self.obj.extract_text_from_tags(soup), {'ter':{'Indicativo Presente': [('eu', 'tenho', True)]}})

    def test_tense_aux_pronoun_conjugation_extraction(self):
         """ """
         soup = BeautifulSoup(html_dict["html_tense_aux_pronoun_conjugation"], 'html.parser')
         self.assertEqual(self.obj.extract_text_from_tags(soup), {'ter':{'Indicativo Pretérito Perfeito Composto': [('eu tenho', 'tido', False)]}})

    def test_wrong_class(self):
         """ """
         soup = BeautifulSoup(html_dict["html_wrong_class"], 'html.parser')
         self.assertEqual(self.obj.extract_text_from_tags(soup), {'ter':{}})

    def test_multiple_tags_extraction(self):
         """ """
         soup = BeautifulSoup(html_dict["html_multiple_tags"], 'html.parser')
         self.assertEqual(self.obj.extract_text_from_tags(soup), {'ter':{'Condicional Futuro do Pretérito Simples': [('eu', 'teria', False), ('tu', 'terias', False), ('ele/ela/você', 'teria', False), ('nós', 'teríamos', False), ('vós', 'teríeis', False), ('eles/elas/vocês', 'teriam', False)]}})
    
    def test_multiple_tags_tense_only_extraction(self):
         """ """
         soup = BeautifulSoup(html_dict["html_multiple_tags_tense_only"], 'html.parser')
         self.assertEqual(self.obj.extract_text_from_tags(soup), {'ter':{'Gerúndio': [(None, 'tendo', False)], 'Particípio': [(None, 'tido', False)]}})

    def test_multiple_tags_tense_missing_extraction(self):
         """ """
         soup = BeautifulSoup(html_dict["html_multiple_tags_missing_tense"], 'html.parser')
         with self.assertRaises(KeyError):
             self.obj.extract_text_from_tags(soup)

class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        self.connection = None
        self.test_db_name = "test_db_populator_create_db"
        self.created_test_db = False

    def tearDown(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def test_server_connection_success(self):
        """ Tests if correct log-in results in a successful conneciton to the MySQL server. """
        connection_args = {
            "host":"localhost", 
            "user":"python_pt", 
            "password":"123"
            }
        self.connection = MySQL_connection.connect_to_mysql_server(connection_args)
        self.assertIsNotNone(self.connection)

    def test_server_connection_failure(self):
        """ Tests if incorrect log-in results in a successful conneciton to the MySQL server. """
        connection_args = {
            "host":"localhost", 
            "user":"not_user", 
            "password":"wrong_password"
            }
        self.connection = MySQL_connection.connect_to_mysql_server(connection_args)
        self.assertIsNone(self.connection)
        

   

class TestDatabaseStorage(unittest.TestCase):
    def setUp(self):
        self.connection = MySQL_connection.connect_to_mysql_server()
        self.cursor = self.connection.cursor()
        self.test_db_name = "test_db_populator_create_db"
    
        self.cursor.execute("SHOW DATABASES")
        databases = [database[0] for database in self.cursor.fetchall()]
        if self.test_db_name in databases:
            raise Exception(f"ERROR: Database '{self.test_db_name}' already exists. Aborting tests to prevent accidental data loss.")
        self.obj = Database(connection=self.connection, data="", create_new_db=True)
        self.obj.create_db(db_name=self.test_db_name)
   
    def tearDown(self):
        self.cursor.execute(f"DROP DATABASE IF EXISTS {self.test_db_name}")
        self.cursor.close()
        self.connection.close()

    def test_database_created(self):
        pass
        # FIXME: if this test fails, final code not ran.
        """ Tests if database is created and populated with tables. """
        self.cursor.execute("SHOW DATABASES")
        databases = [database[0] for database in self.cursor.fetchall()]
        self.assertIn(self.test_db_name, databases)

    def test_database_populated(self):
        self.cursor.execute(f"USE {self.test_db_name}")
        self.cursor.execute("SHOW TABLES")
        tables = [table[0] for table in self.cursor.fetchall()]
        # TODO: populate these tables.
        # TODO: test populate these tables.
        self.assertIn("verb", tables)
        self.assertIn("pronoun", tables)
        self.assertIn("tense", tables)
        self.assertIn("conjugation", tables)
    
    def test_single_row_insertion(self):
        """ A test to see if data is correctly accepted and stored in the appropriate tables. """
        dataset = dataset_dict["single_verb"]
        self.obj.data = dataset
        # print(self.obj.data)
        self.obj.store_row(data=self.obj.data)
        # TODO: populate these tables.
        # self.cursor.execute("SELECT * FROM verb")
        # self.cursor.execute("SELECT * FROM pronoun")
        # self.cursor.execute("SELECT * FROM tense")
        self.cursor.execute("SELECT * FROM conjugation")
        rows = [row for row in self.cursor.fetchall()]
        print("rows: ", rows)
        
        

# 119 + 21

if __name__ == '__main__':
    unittest.main()

# for database we may use 'test fixture'

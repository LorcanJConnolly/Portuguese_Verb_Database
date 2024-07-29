import unittest
from bs4 import BeautifulSoup
from scraper import Scraper
from sample_html import html_dict
from db_populator import Database
import MySQL_connection

class TestHtmlExtraction(unittest.TestCase):

    def test_missing_url(self):
        """Test that an invalid or non-functioning url returns None."""
        missing_url = Scraper(url="123")
        self.assertIsNone(missing_url.get_html())

    def test_sample_url(self):
        """Test that a valid url from another webnsite returns a BeautifulSoup Object."""
        sample_url = Scraper(url="https://docs.scrapy.org/en/latest/_static/selectors-sample1.html")
        self.assertIsInstance(sample_url.get_html(), BeautifulSoup)

    def test_target_url(self):
        """Test that a valid url from Reverso returns a BeautifulSoup Object."""
        target_url = Scraper(url="https://conjugator.reverso.net/conjugation-portuguese-verb-ter.html")
        self.assertIsInstance(target_url.get_html(), BeautifulSoup)

    def test_error_raised(self):    
        """Test that checks correct Error is raised for missing url."""
        missing_url = Scraper("123")
        with self.assertRaises(ValueError): 
            missing_url.parse()
        
class TestTextExtractionFromTags(unittest.TestCase):
    # FIXME: Test documentation.
    def setUp(self) -> None:
        """Verb used for testing is ter."""
        self.obj = Scraper("")
    
    def test_tense_only_extraction(self):
        """Test for extracting the tense from a tag."""
        soup = BeautifulSoup(html_dict["html_tense"], 'html.parser')
        self.assertEqual(self.obj.extract_text_from_tags(soup), {'Indicativo Presente': []})

    def test_tense_pronoun_conjugation_extraction(self):
         """ """
         soup = BeautifulSoup(html_dict["html_tense_pronoun_conjugation"], 'html.parser')
         self.assertEqual(self.obj.extract_text_from_tags(soup), {'Indicativo Presente': [('eu', 'tenho', True)]})

    def test_tense_aux_pronoun_conjugation_extraction(self):
         """ """
         soup = BeautifulSoup(html_dict["html_tense_aux_pronoun_conjugation"], 'html.parser')
         self.assertEqual(self.obj.extract_text_from_tags(soup), {'Indicativo Pretérito Perfeito Composto': [('eu tenho', 'tido', False)]})

    def test_wrong_class(self):
         """ """
         soup = BeautifulSoup(html_dict["html_wrong_class"], 'html.parser')
         self.assertEqual(self.obj.extract_text_from_tags(soup), {})

    def test_multiple_tags_extraction(self):
         """ """
         soup = BeautifulSoup(html_dict["html_multiple_tags"], 'html.parser')
         self.assertEqual(self.obj.extract_text_from_tags(soup), {'Condicional Futuro do Pretérito Simples': [('eu', 'teria', False), ('tu', 'terias', False), ('ele/ela/você', 'teria', False), ('nós', 'teríamos', False), ('vós', 'teríeis', False), ('eles/elas/vocês', 'teriam', False)]})
    
    def test_multiple_tags_tense_only_extraction(self):
         """ """
         soup = BeautifulSoup(html_dict["html_multiple_tags_tense_only"], 'html.parser')
         self.assertEqual(self.obj.extract_text_from_tags(soup), {'Gerúndio': [(None, 'tendo', False)], 'Particípio': [(None, 'tido', False)]})

    def test_multiple_tags_tense_missing_extraction(self):
         """ """
         soup = BeautifulSoup(html_dict["html_multiple_tags_missing_tense"], 'html.parser')
         with self.assertRaises(KeyError):
             self.obj.extract_text_from_tags(soup)

class TestDatabaseStorage(unittest.TestCase):
    """
    First the input would request a database name from the user.
        If one doesn't exist -> ask if they would like to create a new one.
        If one does exist -> we add to this one.
    Also ask if they would like a JSON file output -> give name.
        If one doesn't exist -> create one.
        If one does exist -> add to it.

    -> Creating new database:
        -> Table structure: 
            -> Table1 -> Verb_keys -> verb_key, root_verb
            -> Table2 -> Tense_keys -> tense_key, tense
            -> Table3 -> Pronoun_keys -> pronoun_key, pronoun   # includes aux pronouns
            -> Table4 -> Conjugations -> key, verb, tense, pronoun, conjugation, irregular
                -> Error can be raised when wrong combination of tense + pronoun (e.g., perfect tense + non-aux pronoun) is requested.


    -> insertion:
        -> catch bugs:
            -> We have the expected input structure in text_dict_structure.py
            -> If There are 21 tenses in the dataset, and those tenses have length: (17*6, 1*1, 3*5, 1*1) then we can assume the input is correct.
            -> If the pronouns/aux pronouns are in the correct order we can assume the input is correct.
            -> If incorrect -> skip this dataset insertion and return the verb (for testing).
    """
    def setUp(self):
        self.connection = None
    
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
        
    def test_existence_of_database_check(self):
        """ Tests if the check for whether a database exists or not. """
        obj = Database(connection="", data="", create_new_db=True)
        self.assertTrue(obj.populate_db())


    def tearDown(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("\nConnection closed.")


    
    # 119 + 21
    


if __name__ == '__main__':
    unittest.main()

# for database we may use 'test fixture'

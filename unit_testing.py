import unittest
from bs4 import BeautifulSoup
from scraper import scraper
from sample_html import html_dict

class TestHtmlExtraction(unittest.TestCase):

    def test_missing_url(self):
        """Test that an invalid or non-functioning url returns None."""
        missing_url = scraper(url="123")
        self.assertIsNone(missing_url.get_html())

    def test_sample_url(self):
        """Test that a valid url from another webnsite returns a BeautifulSoup Object."""
        sample_url = scraper(url="https://docs.scrapy.org/en/latest/_static/selectors-sample1.html")
        self.assertIsInstance(sample_url.get_html(), BeautifulSoup)

    def test_target_url(self):
        """Test that a valid url from Reverso returns a BeautifulSoup Object."""
        target_url = scraper(url="https://conjugator.reverso.net/conjugation-portuguese-verb-ter.html")
        self.assertIsInstance(target_url.get_html(), BeautifulSoup)

    def test_error_raised(self):    
        """Test that checks correct Error is raised for missing url."""
        missing_url = scraper("123")
        with self.assertRaises(ValueError): 
            missing_url.parse()
        
class TestTextExtractionFromTags(unittest.TestCase):
    # FIXME: tests
    def setUp(self) -> None:
        """Verb used for testing is ter."""
        self.obj = scraper("")
    
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

    # def test_multiple_tags_tense_missing_extraction(self):
    #      """ """
    #      self.assertEqual(html_dict["html_multiple_tags_missing_tense"], {'Gerúndio': [(None, 'tendo', False)], 'Particípio': [(None, 'tido', False)]})

    # 119 + 21


if __name__ == '__main__':
    unittest.main()

# for database we may use 'test fixture'

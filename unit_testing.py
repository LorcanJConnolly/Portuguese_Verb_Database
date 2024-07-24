import unittest
from scraper import scraper

# obj = scraper()

# assert obj.get_html() == True

class ScraperTest(unittest.TestCase):

    def test_extract_html(self):
        scraper_object = scraper()
        self.assertTrue(scraper_object.get_html())

if __name__ == '__main__':
    unittest.main()

# for database we may use 'test fixture'

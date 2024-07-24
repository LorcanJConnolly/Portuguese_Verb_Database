import unittest
from scraper import scraper

# obj = scraper()

# assert obj.get_html() == True

class ScraperTest(unittest.TestCase):

    def test_extract_html(self):
        scraper_object1, scraper_object2 = scraper(url=None), scraper(url="str")
        self.assertFalse(scraper_object1.get_html())
        self.assertTrue(scraper_object2.get_html())



if __name__ == '__main__':
    unittest.main()

# for database we may use 'test fixture'

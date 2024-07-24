import unittest
from scraper import scraper

# obj = scraper()

# assert obj.get_html() == True

class ScraperTest(unittest.TestCase):

    def test_extract_html(self):
        scraper_object1, scraper_object2 = scraper(url="123"), scraper(url="https://docs.scrapy.org/en/latest/_static/selectors-sample1.html")
        self.assertIsNone(scraper_object1.get_html())
        self.assertIsNotNone(scraper_object2.get_html())



if __name__ == '__main__':
    unittest.main()

# for database we may use 'test fixture'

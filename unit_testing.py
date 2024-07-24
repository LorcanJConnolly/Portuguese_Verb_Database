# import unittest
from scraper import scraper

assert scraper.get_html("https://docs.scrapy.org/en/latest/_static/selectors-sample1.html") == True

# class ScraperTest(unittest.TestCase):

#     def test_extract_html(self):
#         self.assertTrue(get_html("https://docs.scrapy.org/en/latest/_static/selectors-sample1.html"))



# for database we may use 'test fixture'

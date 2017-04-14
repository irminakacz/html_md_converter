import unittest
from bs4 import BeautifulSoup
import urllib
from Converter import Converter

class TestConverter(unittest.TestCase):


    def setUp(self):
        self.converter = Converter()
        page = urllib.request.urlopen(
            "http://blog.cleancoder.com/uncle-bob/2017/01/11/TheDarkPath.html")
        self.soup = BeautifulSoup(page, 'html.parser')


    def test_creating_converter(self):
        self.assertIsNotNone(self.converter)


    def test_clear_head(self):
        self.soup = self.converter.clear_head(self.soup)
        self.assertIsNone(self.soup.head)


    def test_clear_footer(self):
        self.soup = self.converter.clear_footer(self.soup)
        self.assertIsNone(self.soup.footer)


    def test_clear_scripts(self):
        self.soup = self.converter.clear_scripts(self.soup)
        self.assertEqual(self.soup.find_all('script'), [])


    def test_clear_empty_divs(self):
        self.soup = self.converter.clear_empty_divs(self.soup)
        empty_divs = []
        for empty_div in self.soup.find_all('div'):
            if len(empty_div.contents) == 0:
                empty_divs.append(empty_div)
        self.assertEqual(empty_divs, [])


    def test_clear_empty_spans(self):
        self.soup = self.converter.clear_empty_spans(self.soup)
        empty_spans = []
        for empty_div in self.soup.find_all('div'):
            if len(empty_div.contents) == 0:
                empty_spans.append(empty_div)
        self.assertEqual(empty_spans, [])

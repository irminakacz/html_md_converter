import unittest
from bs4 import BeautifulSoup
import urllib
from Converter import Converter

class TestConverter(unittest.TestCase):


    def setUp(self):
        self.converter = Converter()


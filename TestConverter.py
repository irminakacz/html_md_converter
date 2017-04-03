import unittest
from Converter import Converter

class TestConverter(unittest.TestCase):

    def test_creating_converter(self):
        converter = Converter()
        self.assertIsNotNone(converter)

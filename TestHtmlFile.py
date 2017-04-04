import unittest
import sys
import os
from HtmlFile import HtmlFile

class TestHtmlFile(unittest.TestCase):

    def setUp(self):

        self.invalid = open('invalid.txt', 'w')
        self.empty = open('empty.html', 'w')
        self.valid = open('valid.html', 'w')

        self.html = "<html>\n<body>\n<h1>Test</h1>\n</body>\n</html>"
        self.valid.write(self.html)

        self.invalid.close()
        self.empty.close()
        self.valid.close()

        self.htmlFile = HtmlFile()


    def test_file_exist_method(self):
        self.assertTrue(self.htmlFile.file_exist(self.valid.name))
        with self.assertRaises(FileNotFoundError) as err:
            self.htmlFile.file_exist("missing.html")
        self.assertRegexpMatches(str(err.exception), 'File "missing.html" not found.')


    def test_is_html_method(self):
        self.assertTrue(self.htmlFile.is_html(self.valid.name))
        with self.assertRaises(TypeError) as err:
            self.htmlFile.is_html(self.invalid.name)
        self.assertRegexpMatches(str(err.exception), "Invalid file format. Expecting HTML format.")


    def test_is_not_empty_method(self):
        self.assertTrue(self.htmlFile.is_not_empty(self.valid.name))
        with self.assertRaises(EOFError) as err:
            self.htmlFile.is_not_empty(self.empty.name)
        self.assertRegexpMatches(str(err.exception), 'File "' + self.empty.name + '" is empty.')


    def test_validate_method(self):
        self.assertTrue(self.htmlFile.validate(self.valid.name))


    def test_to_string_method(self):
        self.assertEqual(self.htmlFile.convert_to_string(self.valid.name), self.html)


    def tearDown(self):
        os.remove(self.invalid.name)
        os.remove(self.empty.name)
        os.remove(self.valid.name)

import unittest
import sys
import os

class TestConverterToMd(unittest.TestCase):


    def setUp(self):
        self.invalid = open('invalid.txt', 'w')
        self.empty = open('empty.html', 'w')
        self.invalid.close()
        self.empty.close()


    def test_help_message(self):
        sys.argv = ['html_to_md.py']
        with self.assertRaises(SystemExit) as err:
            exec(open('html_to_md.py').read())
        self.assertEqual(err.exception.code, """HTML to markdown converter in Python\n\
usage:
    python3 html_to_md.py -f file\n\
    python3 html_to_md.py -u url""")


    def test_missing_file(self):
        sys.argv = ['html_to_md.py', '-f', 'missing.html']
        with self.assertRaises(SystemExit) as err:
            exec(open('html_to_md.py').read())
        self.assertRegexpMatches(str(err.exception.code), 'File "missing.html" not found.')


    def test_invalid_file_format(self):
        sys.argv = ['html_to_md.py', '-f', self.invalid.name]
        with self.assertRaises(SystemExit) as err:
            exec(open('html_to_md.py').read())
        self.assertRegexpMatches(str(err.exception.code), "Invalid file format. Expecting HTML format.")


    def test_empty_file(self):
        sys.argv = ['html_to_md.py', '-f', self.empty.name]
        with self.assertRaises(SystemExit) as err:
            exec(open('html_to_md.py').read())
        self.assertRegexpMatches(str(err.exception.code), 'File "' + self.empty.name + '" is empty.')


    def tearDown(self):
        os.remove(self.invalid.name)
        os.remove(self.empty.name)


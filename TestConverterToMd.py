import unittest
import sys
import os

class TestConverterToMd(unittest.TestCase):

    def setUp(self):
        self.invalid = open('invalid.txt', 'w')
        self.empty = open('empty.html', 'w')

    def test_missing_filename(self):
        sys.argv = ['convert_to_md.py']
        with self.assertRaises(SystemExit) as err:
            exec(open('convert_to_md.py').read())
        self.assertEqual(err.exception.code, "Missing filename.")

    def test_missing_file(self):
        sys.argv = ['convert_to_md.py', 'missing.html']
        with self.assertRaises(SystemExit) as err:
            exec(open('convert_to_md.py').read())
        self.assertRegexpMatches(str(err.exception.code), 'File "missing.html" not found.')

    def test_invalid_file_format(self):
        sys.argv = ['convert_to_md.py', self.invalid.name]
        with self.assertRaises(SystemExit) as err:
            exec(open('convert_to_md.py').read())
        self.assertRegexpMatches(str(err.exception.code), "Invalid file format. Expecting HTML format.")

    def test_empty_file(self):
        sys.argv = ['convert_to_md.py', self.empty.name]
        with self.assertRaises(SystemExit) as err:
            exec(open('convert_to_md.py').read())
        self.assertRegexpMatches(str(err.exception.code), 'File "' + self.empty.name + '" is empty.')

    def tearDown(self):
        self.invalid.close()
        self.empty.close()
        os.remove(self.invalid.name)
        os.remove(self.empty.name)


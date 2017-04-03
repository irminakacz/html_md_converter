import unittest
import sys

class TestConverterToMd(unittest.TestCase):

    def test_missing_filename(self):
        sys.argv = ['convert_to_md.py']
        with self.assertRaises(SystemExit) as err:
            exec(open('convert_to_md.py').read())
        self.assertEqual(err.exception.code, "Missing filename.")

    def test_missing_file(self):
        sys.argv = ['convert_to_md.py', 'file.html']
        with self.assertRaises(SystemExit) as err:
            exec(open('convert_to_md.py').read())
        self.assertEqual(err.exception.code, 'File "file.html" not found.')


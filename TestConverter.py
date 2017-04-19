import unittest
from bs4 import BeautifulSoup
import urllib
from Converter import Converter
import htmlmin

class TestConverter(unittest.TestCase):


    def setUp(self):
        self.converter = Converter()


    def test_is_forming_quote(self):
        html = "<blockquote>Think for yourself, question authority</blockquote>"
        soup = BeautifulSoup(html, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], "> Think for yourself, question authority")


    def test_forming_simple_table(self):
        html = "<table><tr><td>1 1</td><td>1 2</td></tr><tr><td>2 1</td><td>2 2</td></tr></table>"
        soup = BeautifulSoup(html, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], "| 1 1 | 1 2 |\n")
        self.assertEqual(soup.contents[1], "| 2 1 | 2 2 |\n")


    def test_forming_simple_table_with_table_head(self):
        html = """
            <table>
                <thead>
                <tr><th>One</th><th>Two</th></tr>
                </thead>
                <tr><td>1 1</td><td>1 2</td></tr>
                <tr><td>2 1</td><td>2 2</td></tr>
            </table>
        """
        minified = htmlmin.minify(html, remove_empty_space=True)
        soup = BeautifulSoup(minified, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], "| One | Two |\n|-----|-----|\n")
        self.assertEqual(soup.contents[1], "| 1 1 | 1 2 |\n")
        self.assertEqual(soup.contents[2], "| 2 1 | 2 2 |\n")


    def test_forming_complex_table(self):
        html = """
            <table>
                <thead>
                <tr><th>One</th><th>Two</th></tr>
                </thead>
                <tr>
                    <td><p>Paragraph1</p></td>
                    <td><em>Emphasis</em></td>
                </tr>
                <tr>
                    <td><ul><li>one</li><li>two</li><li>three</li></td>
                    <td><a href="www.example.com">link</a></td>
                </tr>
            </table>
        """
        minified = htmlmin.minify(html, remove_empty_space=True)
        soup = BeautifulSoup(minified, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], "| One | Two |\n|-----|-----|\n")
        self.assertEqual(soup.contents[1], "| Paragraph1 | *Emphasis* |\n")
        self.assertEqual(soup.contents[2], "| - one\n- two\n- three\n | [link](www.example.com) |\n")


    def test_forming_link(self):
        html = '<a href="www.example.com" title="example">link</a>'
        soup = BeautifulSoup(html, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], '[link](www.example.com "example")')


    def test_forming_simple_unordered_list(self):
        html = """
        <ul>
            <li>one</li>
            <li>two</li>
            <li>three</li>
        </ul>
        """
        minified = htmlmin.minify(html, remove_empty_space=True)
        soup = BeautifulSoup(minified, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], '- one\n')
        self.assertEqual(soup.contents[1], '- two\n')
        self.assertEqual(soup.contents[2], '- three\n')


    def test_forming_simple_ordered_list(self):
        html = """
        <ol>
            <li>one</li>
            <li>two</li>
            <li>three</li>
        </ol>
        """
        minified = htmlmin.minify(html, remove_empty_space=True)
        soup = BeautifulSoup(minified, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], '1. one\n')
        self.assertEqual(soup.contents[1], '2. two\n')
        self.assertEqual(soup.contents[2], '3. three\n')


    def test_forming_complex_list(self):
        html = """
        <ol>
            <li>one</li>
            <li><ul>
                <li>item1</li>
                <li>item2</li>
                <li>item3</li>
            </ul></li>
            <li>two</li>
            <li>three</li>
        </ol>
        """
        minified = htmlmin.minify(html, remove_empty_space=True)
        soup = BeautifulSoup(minified, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], '1. one\n')
        self.assertEqual(soup.contents[1], '- item1\n')
        self.assertEqual(soup.contents[2], '- item2\n')
        self.assertEqual(soup.contents[3], '- item3\n')
        self.assertEqual(soup.contents[4], '2. two\n')
        self.assertEqual(soup.contents[5], '3. three\n')



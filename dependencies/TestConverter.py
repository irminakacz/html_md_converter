import unittest
from bs4 import BeautifulSoup
import bs4
import urllib
from dependencies.Converter import Converter
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
        self.assertEqual(soup.contents[0], "| One | Two |\n|---|---|\n")
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
        self.assertEqual(soup.contents[0], "| One | Two |\n|---|---|\n")
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
            <li>two<ul>
                    <li>item1</li>
                    <li>item2</li>
                    <li>item3</li>
            </ul></li>
            <li>three</li>
        </ol>
        """
        minified = htmlmin.minify(html, remove_empty_space=True)
        soup = BeautifulSoup(minified, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], '1. one\n')
        self.assertEqual(soup.contents[1], '2. two\n- item1\n- item2\n- item3\n')
        self.assertEqual(soup.contents[2], '3. three\n')


    def test_forming_image_with_all_attributes(self):
        html = '<img src="www.example.com" alt="text" title="title">'
        soup = BeautifulSoup(html, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], '![text](www.example.com "title")')


    def test_forming_image_with_title_attribute(self):
        html = '<img src="www.example.com" title="title">'
        soup = BeautifulSoup(html, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], '![](www.example.com "title")')


    def test_forming_image_with_alt_attribute(self):
        html = '<img src="www.example.com" alt="text">'
        soup = BeautifulSoup(html, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], '![text](www.example.com)')


    def test_forming_headers(self):
        html = """
        <h1>header1</h1>
        <h2>header2</h2>
        <h3>header3</h3>
        <h4>header4</h4>
        <h5>header5</h5>
        <h6>header6</h6>
        """
        minified = htmlmin.minify(html, remove_empty_space=True)
        soup = BeautifulSoup(minified, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], '\n# header1\n')
        self.assertEqual(soup.contents[1], '\n## header2\n')
        self.assertEqual(soup.contents[2], '\n### header3\n')
        self.assertEqual(soup.contents[3], '\n#### header4\n')
        self.assertEqual(soup.contents[4], '\n##### header5\n')
        self.assertEqual(soup.contents[5], '\n###### header6\n')


    def test_appling_emphasis(self):
        html = """
        <em>italic</em>
        <strong>bold</strong>
        <del>deleted</del>
        <code>code</code>
        """
        minified = htmlmin.minify(html, remove_empty_space=True)
        soup = BeautifulSoup(minified, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], '*italic*')
        self.assertEqual(soup.contents[1], '__bold__')
        self.assertEqual(soup.contents[2], '~~deleted~~')
        self.assertEqual(soup.contents[3], '`code`')


    def test_inserting_horizontal_line(self):
        html = "<hr>"
        soup = BeautifulSoup(html, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], '\n\n----\n\n')


    def test_breaking_line(self):
        html = "<br><br>"
        soup = BeautifulSoup(html, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], '\n\n')


    def test_unwrapping_contents(self):
        html = "<p>Hello<h1>Header</h1><ul><li>one</li><li>two</li></p>"
        soup = BeautifulSoup(html, 'html.parser')
        self.converter.convert(soup)
        self.assertEqual(soup.contents[0], 'Hello\n# Header\n- one\n- two\n')



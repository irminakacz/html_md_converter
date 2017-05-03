import unittest
from Refiner import Refiner
import bs4
from bs4 import BeautifulSoup
from bs4.element import Tag
import htmlmin

class TestHtmlFile(unittest.TestCase):


    def setUp(self):
        self.refiner = Refiner()


    def test_if_nodes_are_convertable(self):
        html = "<div><span></span><h1>Title</h1></div>"
        soup = BeautifulSoup(html, 'html.parser')
        self.assertFalse(self.refiner.convertable(soup.span))
        self.assertTrue(self.refiner.convertable(soup.h1))


    def test_if_all_children_are_empty_(self):
        html = "<div><span></span></div>"
        soup = BeautifulSoup(html, 'html.parser')
        self.assertTrue(self.refiner.all_children_empty(soup.span))
        self.assertFalse(self.refiner.all_children_empty(soup.div))


    def test_has_children_method(self):
        html = "<div><span></span><h1>Title</h1></div>"
        soup = BeautifulSoup(html, 'html.parser')
        self.assertTrue(self.refiner.has_children(soup.div))
        self.assertTrue(self.refiner.has_children(soup.h1))
        self.assertFalse(self.refiner.has_children(soup.span))


    def test_refine_node_on_node_with_empty_children(self):
        html = "<span></span>"
        soup = BeautifulSoup(html, 'html.parser')
        self.refiner.refine_node(soup.span)
        self.assertFalse(soup.span)


    def test_refine_node_on_convertable_node(self):
        html = "<h1>Title</h1>"
        soup = BeautifulSoup(html, 'html.parser')
        self.refiner.refine_node(soup.h1)
        self.assertTrue(soup.h1)


    def test_refine_node_on_unwrapable_node(self):
        html = "<span><p>Hello<p></span>"
        soup = BeautifulSoup(html, 'html.parser')
        self.refiner.refine_node(soup.span)
        self.assertFalse(soup.span)
        self.assertTrue(soup.p)


    def test_refine_empty_nonconvertable_tag(self):
        html = "<p><span></span><div></div><h1>Hello</h1></p>"
        soup = BeautifulSoup(html, 'html.parser')
        self.refiner.refine_tag(soup.p)
        self.assertFalse(soup.span)
        self.assertFalse(soup.div)
        self.assertTrue(soup.h1)

    def test_refine_navigable_strings(self):
        html = "<span>Span</span><div>Div<h1>Hello</h1></div>"
        soup = BeautifulSoup(html, 'html.parser')
        self.refiner.refine_other_strings(soup.span)
        self.assertTrue(self.refiner.all_children_empty(soup.span))
        self.refiner.refine_other_strings(soup.div)
        self.assertTrue(soup.div.h1)
        self.assertEqual(soup.div.contents[0], '')
        self.assertEqual(soup.div.contents[1], soup.div.h1)


    def test_leaving_out_strings_when_refine_tags(self):
        html = "NavigableString"
        soup = BeautifulSoup(html, 'html.parser')
        self.refiner.refine_tags(soup)
        self.assertEqual(soup.text, "NavigableString")



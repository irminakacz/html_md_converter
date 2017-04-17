import bs4
from bs4 import BeautifulSoup
import htmlmin

class Converter:


    basic = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'em', 'strong', 'del',
                'code', 'ol', 'ul', 'li', 'a', 'img', 'table', 'thead', 'tr',
                'th', 'tbody', 'td', 'blockquote', 'hr', 'br', 'p']


    def convert(self, html):
        minified = htmlmin.minify(html, remove_empty_space=True)
        soup = BeautifulSoup(minified, 'html.parser')
        self.refine(soup)
        #markdown = self.swap_tags(soup)
        return str(soup.prettify())


    def refine(self, node):
        self.refine_children(node)
        self.refine_node(node)


    def refine_children(self, node):
        for child in node:
            if isinstance(child, bs4.element.Tag):
                if self.has_children(child):
                    self.refine(child)
                elif not self.convertable(child):
                    child.replace_with('')
            elif not self.convertable(node):
                child.replace_with('')


    def refine_node(self, node):
        if not self.convertable(node):
            if self.has_children(node):
                if self.all_children_empty(node):
                    node.replace_with('')
                elif node.parent:
                    node.unwrap()
            else:
                node.replace_with('')


    def has_children(self, node):
        if len(node.contents) > 0:
            return True
        return False


    def all_children_empty(self, node):
        for child in node:
            if child != '':
                return False
        return True


    def convertable(self, node):
        if node.name in self.basic:
            return True
        return False


converter = Converter()
f = open("cleancode.html", "r")
html = f.read()
output = converter.convert(html)

good_one = open("output.html", "r")
if (good_one.read() == output):
    print("OK")
else:
    print(output)

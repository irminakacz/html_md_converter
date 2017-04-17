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
                if len(child.contents) > 0:
                    self.refine(child)
                elif self.convertable(child):
                    continue
                else:
                    child.replace_with('')


    def refine_node(self, node):
        if self.convertable(node):
            return

        if len(node.contents) > 0:
            all_children_empty = True
            for child in node:
                if child != '':
                    all_children_empty = False

            if all_children_empty:
                node.replace_with('')
            elif node.parent:
                node.unwrap()
        else:
            node.replace_with('')


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

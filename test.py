import bs4
from bs4 import BeautifulSoup
import htmlmin

basic = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'em', 'strong', 'del',
            'code', 'ol', 'ul', 'li', 'a', 'img', 'table', 'thead', 'tr',
            'th', 'tbody', 'td', 'blockquote', 'hr', 'br', 'p']

def convertable(node):
    if node.name in basic:
        return True
    return False

f = open("cleancode.html", "r")
html = f.read()
minified = htmlmin.minify(html, remove_empty_space=True)
soup = BeautifulSoup(minified, 'html.parser')


def refine(node):
    for child in node:
        if isinstance(child, bs4.element.Tag):
            if len(child.contents) > 0:
                refine(child)
            else:
                if convertable(child):
                    continue
                else:
                    child.replace_with('')
        else:
            if convertable(child.parent):
                continue
            else:
                child.parent.replace_with('')


refine(soup)
print(soup.prettify())

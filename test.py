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
soup = soup.head

def refine(node):

    for child in node:
        if isinstance(child, bs4.element.Tag):
            if len(child.contents) > 0:
                refine(child)
            else:
                if convertable(child):
                    continue
                else:
                    print("to be erased: " + str(child))
                    child.replace_with('')
        else:
            if convertable(child.parent):
                continue
            else:
                print("to be erased through erasing parent: " + str(child))
                child.parent.replace_with('')

        # when we're done with the children
        # we take a look at the node itself

        # delete or unwarp only when it's not convertable
        if not convertable(node):
            # have children?
            if len(node.contents) > 0:

                # if they are all empty - kill it
                all_children_empty = True

                for child in node:
                    if child != '':
                        all_children_empty = False

                if all_children_empty:
                    print("to be erased by erasing not having children: " + str(node))
                    node.replace_with('')

                # if they are all not convertable - kill it
                all_children_non_convertable = True

                for child in node:
                    if convertable(child):
                        all_children_non_convertable = False

                if all_children_non_convertable:
                    pass
                    #node.replace_with('')

                else:
                    pass
                    #print("children: " + str(node.contents[0]))
                    #print("should be unwrapped: " + str(node.name))
            else:
                # no children? kill it
                node.replace_with('')

refine(soup)
print(soup.prettify())

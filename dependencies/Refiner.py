import bs4
from bs4 import BeautifulSoup
from bs4.element import Tag
import htmlmin

class Refiner:
    """Refiner"""

    basic = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'em', 'strong', 'del',
                'code', 'ol', 'ul', 'li', 'a', 'img', 'table', 'thead', 'tr',
                'th', 'tbody', 'td', 'blockquote', 'hr', 'br', 'p']


    def refine(self, node):
        """refine

        :param node:
        """
        self.refine_tags(node)
        self.refine_other_strings(node)
        self.refine_node(node)


    def refine_tags(self, node):
        """refine_tags

        :param node:
        """
        tag_children = filter(lambda child: isinstance(child, Tag), node)

        for tag in tag_children:
            self.refine_tag(tag)


    def refine_other_strings(self, node):
        """refine_other_strings

        :param node:
        """
        navigable_strings = filter(lambda child: not isinstance(child, Tag), node)
        other_strings = filter(lambda child: not self.convertable(node), navigable_strings)

        for string in other_strings:
            if string.parent.name != 'div':
                if string.parent.name != 'span':
                    string.replace_with('')


    def refine_tag(self, child):
        """refine_tag

        :param child:
        """
        if self.has_children(child):
            self.refine(child)
        elif not self.convertable(child):
            child.replace_with('')


    def refine_node(self, node):
        """refine_node

        :param node:
        """
        if self.convertable(node):
            return

        if self.all_children_empty(node):
            node.replace_with('')
        if node.parent:
            node.unwrap()


    def has_children(self, node):
        """has_children

        :param node:
        """
        return len(node.contents) > 0


    def all_children_empty(self, node):
        """all_children_empty

        :param node:
        """
        empty_children = filter(lambda n: n != '', node)
        return len(list(empty_children)) == 0


    def convertable(self, node):
        """convertable

        :param node:
        """
        return node.name in self.basic

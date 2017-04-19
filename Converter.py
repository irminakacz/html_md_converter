import bs4
from bs4 import BeautifulSoup
from bs4.element import Tag
import htmlmin
from Refiner import Refiner

class Converter:


    def convert_html_to_markdown(self, html):
        minified = self.minify_html(html)
        nodes = self.transform_into_nodes(minified)
        Refiner().refine(nodes)
        self.convert(nodes)
        return str(nodes)


    def minify_html(self, html):
        return htmlmin.minify(html, remove_empty_space=True)


    def transform_into_nodes(self, html):
        return BeautifulSoup(html, 'html.parser')


    def convert(self, node):
        if not isinstance(node, Tag):
            return

        for child in node:
            self.convert(child)
        self.convert_node(node)


    def convert_node(self, node):
        nodes_to_swap = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                         'em', 'strong', 'del', 'code', 'ol',
                         'ul', 'a', 'img', 'table', 'blockquote',
                         'hr', 'br', 'p']

        emphasis = ['em', 'stron', 'del', 'code']
        headers = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

        if node.name == 'br':
            self.break_line(node)
        if node.name == 'hr':
            self.insert_horizontal_line(node)
        if node.name in emphasis:
            self.apply_emphaisis(node)
        if node.name in headers:
            self.form_header(node)
        if node.name == 'img':
            self.form_image(node)
        if node.name == 'ol':
            self.form_ordered_list(node)
        if node.name == 'ul':
            self.form_unordered_list(node)
        if node.name == 'a':
            self.form_link(node)
        if node.name == 'table':
            self.form_table(node)
        if node.name == 'blockquote':
            self.form_quote(node)
        if node.name == 'p':
            node.replace_with(self.unwrap_contents(node))


    def unwrap_contents(self, node):
        text = ''
        for contents in node.contents:
            text += str(contents)
        return text


    def break_line(self, node):
        node.replace_with('\n' + self.unwrap_contents(node))


    def insert_horizontal_line(self, node):
        node.replace_with('\n\n----\n\n' + self.unwrap_contents(node))


    def apply_emphaisis(self, node):
        if node.name == 'em':
            node.replace_with('*' + self.unwrap_contents(node) + '*')

        if node.name == 'strong':
            node.replace_with('__' + self.unwrap_contents(node) + '__')

        if node.name == 'del':
            node.replace_with('~~' + self.unwrap_contents(node) + '~~')

        if node.name == 'code':
            node.replace_with('`' + self.unwrap_contents(node) + '`')


    def form_header(self, node):
        header_type = int(node.name[1])
        node.replace_with('\n' + '#' * header_type + ' ' +
                          self.unwrap_contents(node) + '\n')


    def form_image(self, node):
        if 'alt' in node.attrs and 'title' in node.attrs:
            node.replace_with('![' + node['alt'] + '](' + node['src'] + ' "' + node['title'] + '")')
        elif 'alt' in node.attrs:
            node.replace_with('![' + node['alt'] + '](' + node['src'] + ')')
        elif 'title' in node.attrs:
            node.replace_with('![](' + node['src'] + ' "' + node['title'] + '")')
        else:
            node.replace_with('![](' + node['src'] + ')')


    def form_ordered_list(self, node):
        order = 1;
        for item in node:
            item.replace_with(str(order) + '. ' + str(item.contents[0]) + '\n')
            order += 1
        node.unwrap()


    def form_unordered_list(self, node):
        for item in node:
            item.replace_with('- ' + str(item.contents[0]) + '\n')
        node.unwrap()


    def form_link(self, node):
        if 'title' in node.attrs:
            node.replace_with('[' + self.unwrap_contents(node) + '](' + node['href']
                              + ' "' + node['title'] + '")')
        else:
            node.replace_with('[' + self.unwrap_contents(node) + '](' + node['href'] + ')')


    def form_table(self, node):
        for row in node:
            if isinstance(row, Tag):
                if row.name == 'thead':
                    self.form_table_head(row)
                    continue
                for cell in row:
                    cell.replace_with('| ' + self.unwrap_contents(cell) + ' ')
                row.replace_with(self.unwrap_contents(row) + '|\n')
        node.unwrap()


    def form_table_head(self, node):
        separator = ''
        for cell in node.tr:
            cell_width = len(self.unwrap_contents(cell)) + 2
            cell.replace_with('| ' + self.unwrap_contents(cell) + ' ')
            separator += '|' + '-' * cell_width
        node.tr.replace_with(self.unwrap_contents(node.tr) + '|\n' + separator + '|\n')
        node.unwrap()


    def form_quote(self, node):
        node.replace_with('> ' + self.unwrap_contents(node))



import bs4
from bs4 import BeautifulSoup
from bs4.element import Tag
import htmlmin
from dependencies.Refiner import Refiner

class Converter:
    def convert_html_to_markdown(self, html):
        minified = self.minify_html(html)
        nodes = self.transconvert_into_nodes(minified)
        Refiner().refine(nodes)
        self.convert(nodes)
        return str(nodes)


    def minify_html(self, html):
        return htmlmin.minify(html, remove_empty_space=True)


    def transconvert_into_nodes(self, html):
        return BeautifulSoup(html, 'html.parser')


    def convert(self, node):
        if not isinstance(node, Tag):
            return

        for child in node:
            self.convert(child)
        self.convert_node(node)


    def convert_node(self, node):
        element_to_forming_func = {
            'em': self.apply_emphasis,
            'strong': self.apply_emphasis,
            'del': self.apply_emphasis,
            'code': self.apply_emphasis,
            'h1': self.convert_header,
            'h2': self.convert_header,
            'h3': self.convert_header,
            'h4': self.convert_header,
            'h5': self.convert_header,
            'h6': self.convert_header,
            'p': self.unwrap_paragraph,
            'br': self.break_line,
            'hr': self.insert_horizontal_line,
            'img': self.convert_image,
            'ol': self.convert_ordered_list,
            'ul': self.convert_unordered_list,
            'a': self.convert_link,
            'table': self.convert_table,
            'blockquote': self.convert_quote,
        }

        if node.name in element_to_forming_func.keys():
            element_to_forming_func[node.name](node)


    def unwrap_paragraph(self, node):
        node.replace_with(self.unwrap_contents(node))


    def unwrap_contents(self, node):
        try:
            return ''.join(node.contents)
        except:
            return ''


    def break_line(self, node):
        node.replace_with('\n' + self.unwrap_contents(node))


    def insert_horizontal_line(self, node):
        node.replace_with('\n\n----\n\n' + self.unwrap_contents(node))


    def apply_emphasis(self, node):
        symbol = {
            'em': '*',
            'strong': '__',
            'del': '~~',
            'code': '`'
        }[node.name]

        node.replace_with(symbol + self.unwrap_contents(node) + symbol)


    def convert_header(self, node):
        header_type = int(node.name[1])
        node.replace_with('\n' + '#' * header_type + ' ' +
                          self.unwrap_contents(node) + '\n')


    def convert_image(self, node):
        if 'alt' in node.attrs and 'title' in node.attrs:
            node.replace_with('![' + node['alt'] + '](' + node['src'] + ' "' + node['title'] + '")' + self.unwrap_contents(node))
        elif 'alt' in node.attrs:
            node.replace_with('![' + node['alt'] + '](' + node['src'] + ')' + self.unwrap_contents(node))
        elif 'title' in node.attrs:
            node.replace_with('![](' + node['src'] + ' "' + node['title'] + '")' + self.unwrap_contents(node))
        else:
            node.replace_with('![](' + node['src'] + ')' + self.unwrap_contents(node))


    def convert_ordered_list(self, node):
        for item in node:
            order = node.index(item) + 1
            item.replace_with(str(order) + '. ' + self.unwrap_contents(item) + '\n')

        self.handle_if_nested(node)


    def convert_unordered_list(self, node):
        for item in node:
            item.replace_with('- ' + self.unwrap_contents(item) + '\n')

        self.handle_if_nested(node)


    def handle_if_nested(self, node):
        if node.parent.name == 'li':
            node.replace_with('\n' + self.unwrap_contents(node)[:-1])
        else:
            node.unwrap()


    def convert_link(self, node):
        if 'title' in node.attrs and 'href' in node.attrs:
            node.replace_with('[' + self.unwrap_contents(node) + '](' + node['href'] + ' "' + node['title'] + '")')
        elif 'href' in node.attrs:
            node.replace_with('[' + self.unwrap_contents(node) + '](' + node['href'] + ')')
        else:
            node.replace_with(self.unwrap_contents(node))


    def convert_table(self, node):
        for row in node:
            if row.name == 'thead':
                self.convert_table_head(row)
                continue
            for cell in row:
                self.convert_table_cell(cell)
            self.convert_table_row(row)
        node.unwrap()


    def convert_table_head(self, node):
        separator = ''
        for cell in node.tr:
            cell.replace_with('| ' + self.unwrap_contents(cell) + ' ')
            separator += '|' + '---'
        node.tr.replace_with(self.unwrap_contents(node.tr) + '|\n' + separator + '|\n')
        node.unwrap()


    def convert_table_cell(self, cell):
        try:
            cell.replace_with('| ' + self.unwrap_contents(cell) + ' ')
        except:
            pass


    def convert_table_row(self, row):
        row.replace_with(self.unwrap_contents(row) + '|\n')


    def convert_quote(self, node):
        node.replace_with('> ' + self.unwrap_contents(node))



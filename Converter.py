from bs4 import BeautifulSoup

class Converter:

    basic = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'em', 'strong', 'del',
                'code', 'ol', 'ul', 'li', 'a', 'img', 'table', 'thead', 'tr',
                'th', 'tbody', 'td', 'blockquote', 'hr', 'br']


    def convert(self, html):
        html = BeautifulSoup(html, 'html.parser')
        html = self.refine(html)
        return html


    def refine(self, html):

        """
        html = self.clear_head(html)
        html = self.clear_footer(html)
        html = self.clear_scripts(html)
        html = self.clear_empty_divs(html)
        html = self.clear_empty_spans(html)
        """
        return html


    def transform(self, html):
        pass


    def clear_head(self, html):
        html.head.decompose()
        return html


    def clear_footer(self, html):
        html.footer.decompose()
        return html


    def clear_scripts(self, html):
        for script in html.find_all('script'):
            script.decompose()
        return html


    def clear_empty_divs(self, html):
        for empty_div in html.find_all('div'):
            if len(empty_div.contents) == 0:
                empty_div.decompose()
        return html


    def clear_empty_spans(self, html):
        for empty_span in html.find_all('span'):
            if len(empty_span.contents) == 0:
                empty_span.decompose()
        return html

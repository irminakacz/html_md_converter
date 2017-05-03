import os

class HtmlFile:
    """HtmlFile"""

    def convert_to_string(self, filename):
        """convert_to_string

        :param filename:
        """
        if self.validate(filename):
            html = open(filename, 'r')
            contents = html.read()
            html.close()
            return contents
        return None


    def validate(self, filename):
        """validate

        :param filename:
        """
        if self.file_exist(filename):
            if self.is_html(filename):
                if self.is_not_empty(filename):
                    return True


    def file_exist(self, filename):
        """file_exist

        :param filename:
        """
        if not(os.path.exists(filename)):
            raise FileNotFoundError('File "' + filename + '" not found.')
            return False
        return True


    def is_html(self, filename):
        """is_html

        :param filename:
        """
        if not(filename.endswith('.html')):
            raise TypeError("Invalid file format. Expecting HTML format.")
            return False
        return True


    def is_not_empty(self, filename):
        """is_not_empty

        :param filename:
        """
        if not(os.path.getsize(filename) > 0):
            raise EOFError('File "' + filename + '" is empty.')
            return False
        return True

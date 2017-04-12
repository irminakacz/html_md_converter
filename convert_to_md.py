import sys
from Converter import Converter
from HtmlFile import HtmlFile

converter = Converter()
htmlFile = HtmlFile()

try:
    filename = sys.argv[1]
except IndexError:
    sys.exit("Missing filename.")

try:
    html = htmlFile.convert_to_string(filename)
except TypeError as err:
    sys.exit(err)
except FileNotFoundError as err:
    sys.exit(err)
except EOFError as err:
    sys.exit(err)

try:
    markdown = converter.convert(html.read())
    #output = open("converted", "w")
    #output.write(markdown)
    #output.close()

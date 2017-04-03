import sys
from Converter import Converter

converter = Converter()

try:
    filename = sys.argv[1]
except IndexError:
    sys.exit("Missing filename.")

try:
    html = open(filename, "r")
except FileNotFoundError as err:
    sys.exit('File "' + filename + '" not found.')

if not(filename.endswith('.html')):
    sys.exit("Invalid file format. Expected html file.")

try:
    markdown = converter.convert(html.read())
    #output = open("converted", "w")
    #output.write(markdown)
finally:
    html.close()
    #markdown.close()

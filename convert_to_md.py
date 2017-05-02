import os
import sys
import urllib
import os.path
from Converter import Converter
from HtmlFile import HtmlFile

def getFile(arg):
    if (mode == "-f"):
        try:
            filename = sys.argv[2]
        except IndexError:
            sys.exit("Missing filename")

    if (mode == "-u"):
        try:
            url = sys.argv[2]
        except IndexError:
            sys.exit("Missing url")

        temp = open("temporary_html_file.html", "w")
        try:
            html = urllib.request.urlopen(url)
        except URLError:
            sys.exit("Invalid url")

        temp.write(html.read().decode('utf-8'))
        filename = temp.name
        temp.close()

    return filename

try:
    mode = sys.argv[1]
except IndexError:
    sys.exit("-f filename | -u url")

try:
    filename = getFile(sys.argv[2])
except IndexError:
    sys.exit("Missing parameters")

try:
    html = HtmlFile().convert_to_string(filename)
except TypeError as err:
    sys.exit(err)
except FileNotFoundError as err:
    sys.exit(err)
except EOFError as err:
    sys.exit(err)


markdown = Converter().convert_html_to_markdown(html)
print(markdown)
output = open("converted.md", "w")
output.write(markdown)
output.close()

if os.path.exists("temporary_html_file.html"):
    os.remove("temporary_html_file.html")

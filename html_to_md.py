import os
import sys
import urllib
import os.path
from Converter import Converter
from HtmlFile import HtmlFile

help_message = """HTML to markdown converter in Python\n\
usage:
    python3 html_to_md.py -f file\n\
    python3 html_to_md.py -u url\n"""

def getFile(mode):
    if (mode == "-f"):
        try:
            filename = sys.argv[2]
        except IndexError:
            sys.exit("Missing filename")

    elif (mode == "-u"):
        try:
            url = sys.argv[2]
        except IndexError:
            sys.exit("Missing url")

        try:
            html = urllib.request.urlopen(url)
        except ValueError:
            sys.exit("Invalid url")

        temp = open("temporary_html_file.html", "w")
        temp.write(html.read().decode('utf-8'))
        filename = temp.name
        temp.close()

    else:
        sys.exit("Invalid mode (must be -f or -u)")

    return filename

############# main script body ############
try:
    mode = sys.argv[1]
except IndexError:
    sys.exit(help_message)

filename = getFile(mode)

try:
    html = HtmlFile().convert_to_string(filename)
except TypeError as err:
    sys.exit(err)
except FileNotFoundError as err:
    sys.exit(err)
except EOFError as err:
    sys.exit(err)

markdown = Converter().convert_html_to_markdown(html)
output = open(filename[:-4] + "md", "w")
output.write(markdown)
output.close()

if os.path.exists("temporary_html_file.html"):
    os.remove("temporary_html_file.html")
###########################################

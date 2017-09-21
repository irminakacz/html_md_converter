# Simple HTML to MARKDOWN converting script

### Requirements
- Python 3.5
- htmlmin (https://pypi.python.org/pypi/htmlmin)

### Converting
##### From file
`python3 html_to_md.py -f path/to/file`
Returns markdown file with the same name as original file into the folder of original file. 

##### From url
`python3 html_to_md.py -u my_url`
Returns markdown file with name containing given url into the folder containing `html_to_md.py`.

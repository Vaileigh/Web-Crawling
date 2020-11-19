  
'''
File        : clean.py
Date        : Wednesday 18th November 2020
Author      : VaileyXO
Description : Crawl web content from html file or website and write in txt file.
Notes       : install bs4 needed
'''

# Python 3

import re
import sys
from urllib.request import urlopen

def identified_html(html):  # This function is to check whether user input is url
    regex = re.compile(
            r'^(?:http|ftp)s?://' # Include http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # Include a domain
            r'localhost|' # Include localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # Include any ip
            r'(?::\d+)?' # Include optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)  # Ignore all cases
    con = re.match(regex, html) is not None     # Return true if url
    con = bool(con)                             # Make sure is boolean
    return con                                  # Return the condition True/False
    
def clean_html(html,filename):
    if(isinstance(html,bytes)):                     # If statement: convert bytes to string if necessary
            html = html.decode('utf-8','ignore')    # Html was decode('utf-8')
    from bs4 import BeautifulSoup                   # Import BeutifulSoup
    html = BeautifulSoup(html, 'html.parser')       # Parse the html
    html = html.get_text()                          # Retrieve text only in html
    
    html = re.sub(r"[\r\n]{2,}", "",html)     # Removes redundant new line
    cleaned = html.strip()                    # Removes any leading
    print ('cleaned= ', cleaned)
    return cleaned

def main():
  if len(sys.argv) != 2:
    print ('usage: ./clean.py file')
    sys.exit(1)
  filename = sys.argv[1]
  
  try:
    if identified_html(filename):           # If statement: user input file is url format
        input_file = urlopen(filename)
    else:                                   # Else statement: user input file is not url format
        input_file = open(filename, 'r')
    
  except (IOError) as ex:
        print('Cannot open ', filename, '\n Error: ', ex)
    
  else:
    html = input_file.read() # read the input file
    cleaned = clean_html(html, filename)
 
    # now prepare the output file
    m = re.search('\w+', filename)
    outfile = m.group()
    if outfile:
      output_file = open(outfile+ '.txt', 'w', encoding="utf-8")    # Add "encoding="utf-8" or not some webpage will occur error
    else:
      output_file = open('cleaned.txt', 'w', encoding="utf-8")      # Error Msg: UnicodeEncodeError: 'charmap' codec can't encode characters in position 0-10: character maps to <undefined>
      
    # write cleaned text to the output
    print(cleaned, file=output_file)
 
  finally:
  	input_file.close()
    
    
if __name__ == '__main__':
  main()

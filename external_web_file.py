from bs4 import BeautifulSoup
from urlparse import urlparse
import sys
import operator

websites = {}

def findExternal(element, attribute):
    global websites

    for tag in soup.findAll(element):
        try:
            fqdn = urlparse(tag[attribute]).netloc
            if not fqdn:
                continue

            if fqdn in websites:
                websites[fqdn] += 1
            else:
                websites[fqdn] = 1
        except:
            continue

soup = BeautifulSoup(open(sys.argv[1]), "lxml")
findExternal('script', 'src')
findExternal('iframe', 'src')
findExternal('window', 'data')

for key in websites:
    print key

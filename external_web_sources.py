from bs4 import BeautifulSoup
from pprint import pprint
from urlparse import urlparse
import lib.gds.pub.burp
import sys
import operator
from lib.cursesmenu.cursesmenu import *
from lib.cursesmenu.cursesmenu.items import *

def findExternal(element, attribute):
    global websites
    global sources
    global source_url

    for tag in soup.findAll(element):
        try:
            fqdn = urlparse(tag[attribute]).netloc
            if not fqdn:
                continue

            if fqdn in websites:
                websites[fqdn] += 1
                if source_url in sources[fqdn]:
                    sources[fqdn][source_url] += 1
                else:
                    sources[fqdn][source_url] = 1
            else:
                websites[fqdn] = 1
                sources[fqdn] = { source_url : 1 }
        except:
            continue

if len(sys.argv) != 2:
    print 'Please provide log file path. python ' + sys.argv[0] + " <log_file>"
    sys.exit()

burp_calls = lib.gds.pub.burp.parse(sys.argv[1])

websites = {}
sources = {}
source_url = ''

menu = CursesMenu("3rd Party Callouts", "")

for call in burp_calls:
    response = call.get_response_body()
    source_url = call.url.netloc + call.url.path
    soup = BeautifulSoup(response, 'lxml')
    findExternal('script', 'src')
    findExternal('iframe', 'src')
    findExternal('window', 'data')
    
top_websites = sorted(websites.items(), key=operator.itemgetter(1), reverse=True)

for i in range(len(top_websites)):
    site = top_websites[i]

    top_url_callouts = sorted(sources[site[0]].items(), key=operator.itemgetter(1), reverse=True)
    website_submenu = CursesMenu("Websites", "Websites that called the domain")
    for url in top_url_callouts:
        website_submenu.append_item(MenuItem(str(url[1]) + ": " + url[0]))

    domain_submenu_item = SubmenuItem(str(site[1]) + ": " + site[0], submenu=website_submenu)
    domain_submenu_item.set_menu(menu)

    menu.append_item(domain_submenu_item)

menu.start()
menu.join()

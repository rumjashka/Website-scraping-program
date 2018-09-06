from urllib.parse import urlparse
import csv
from bs4 import BeautifulSoup
import requests
import time

DOMAIN = 'www.bol.com'
HOST = 'http://' + DOMAIN
FORBIDDEN_PREFIXES = ['#', 'tel:', 'mailto:']
suffixes = [ '.jpg', '.pdf', '.mp3', '.png']
links = set()
f = csv.writer(open('html-links.csv', 'w'))
f.writerow(['Link'])

def add_all_links_recursive(url):
    links_to_handle_recursive = []
    request = requests.get(url)
    soup = BeautifulSoup(request.content, "lxml")

    if request.status_code == 429:
        return

    if 'https://www.googletagmanager.com/gtm.js' not in request.content.decode(errors='replace'):
        print(url)
        f.writerow([url])

    for tag_a in soup.find_all('a'):
        link = tag_a.get('href')


        if link is None:
            continue

        if all(not link.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):

            if all(not link.endswith(suffix) for suffix in suffixes):

                if link.startswith('/') and not link.startswith('//'):
                    link = HOST + link

                if urlparse(link).netloc == DOMAIN and link not in links:
                    links.add(url)
                    links_to_handle_recursive.append(link)





    for link in links_to_handle_recursive:
        add_all_links_recursive(link)


def main():
    add_all_links_recursive(HOST + '/')

if __name__ == '__main__':
    main()
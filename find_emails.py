import requests
from bs4 import BeautifulSoup

with open('urls.xml', 'r') as xml_file:
    soup = BeautifulSoup(xml_file, 'xml')

for url in soup.find_all('url'):
    r = requests.get(url.text)

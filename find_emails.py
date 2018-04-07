import requests
import re
from bs4 import BeautifulSoup


def find_emails(url, depth):
    if depth < 3:
        r = requests.get(url.text)
        soup = BeautifulSoup(r.text, 'lxml')
        email_pattern = re.compile('[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.com')
        for email in email_pattern.findall(soup.get_text()):
            add_email(email)

def add_email(email):
    if email not in emails:
        emails.append(email)


with open('urls.xml', 'r') as xml_file:
    soup = BeautifulSoup(xml_file, 'xml')

emails = []
for url in soup.find_all('url'):
   find_emails(url, 0)

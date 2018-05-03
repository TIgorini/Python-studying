import requests
import re
from bs4 import BeautifulSoup

dict = {}
emails = []


def find_emails(url, depth):
    if depth < 2:
        print(url)
        try:
            r = requests.get(url, timeout=10)
        except requests.exceptions.Timeout:
            print('    {} does not response'.format(url))
            return
        soup = BeautifulSoup(r.text, 'lxml')
        email_pattern = re.compile(
            '[A-Z0-9_]+@[A-Z0-9_]+\.[A-Z_]{2,}',
            re.IGNORECASE
        )

        for email in email_pattern.findall(soup.get_text()):
            print('    email found: {}'.format(email))
            add_email(email)

        pattern = re.compile('^(http|https)', re.IGNORECASE)

        for link in soup.find_all('a', href=True):
            uri = link.get('href')
            if pattern.match(uri) and not(uri in dict):
                dict[uri] = 1
                find_emails(uri, depth + 1)


def add_email(email):
    if email not in emails:
        emails.append(email)


def emails_to_xml():
    soup = BeautifulSoup('<data></data>', 'xml')
    root = soup.data
    for email in emails:
        tag = soup.new_tag('email')
        tag.string = email
        root.append(tag)
    with open('emails.xml', 'w') as xml:
        xml.write(soup.prettify())


with open('urls.xml', 'r') as xml_file:
    soup = BeautifulSoup(xml_file, 'xml')

for url in soup.find_all('url'):
    find_emails(url.text, 0)
emails_to_xml()

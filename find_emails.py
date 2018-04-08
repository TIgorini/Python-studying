import requests
import re
from bs4 import BeautifulSoup


def find_emails(url, depth):
    if depth < 1:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        # запили норм регулярку
        email_pattern = re.compile('[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.ru')
        for email in email_pattern.findall(soup.get_text()):
            add_email(email)

        #пока что работает не очень
        pattern = re.compile('^(http|https)')
        for link in soup.find_all('a', href=True):
            if pattern.match(link.get('href')):
                find_emails(link.get('href'), depth + 1)
            else:
                find_emails(url + link.get('href'), depth + 1)


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

emails = []
for url in soup.find_all('url'):
    find_emails(url.text, 0)
emails_to_xml()

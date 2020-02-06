import requests
from bs4 import BeautifulSoup
import re

def has_class_but_no_id(tag):
    return tag.has_attr('class')

url = 'https://www.edmunds.com/acura/tlx/2020/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
page = requests.get(url,headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.find_all(string=re.compile('Available styles include')))
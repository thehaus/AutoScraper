import requests
import dbservice
from bs4 import BeautifulSoup

baseurl = 'https://www.edmunds.com'
modelurlfile = 'modelurls.txt'
trimsfile = 'modeltrims.txt'
carbrandsfile = 'carbrands.txt'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def html_element_is_car_model_url(tag):
    if tag.has_attr('href') and tag.has_attr('data-tracking-id'):
        return tag['data-tracking-id'] == 'view_content_models'
    return False

def html_element_is_car_trim(tag):
    if tag.name=='div' and tag.has_attr('class'):
        return tag['class'] == 'd-flex justify-content-between separator pb-1'
    return False

def populate_car_model_url_list():
    for carbrand in dbservice.readfromdb(carbrandsfile):
        url = baseurl + '/' + carbrand + '/'
        page = requests.get(url,headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        for carmodelurl in soup.find_all(html_element_is_car_model_url):
            dbservice.writetodb(modelurlfile,carmodelurl.get('href'))

def populate_car_models_and_trims():
    for carmodelurl in dbservice.readfromdb(modelurlfile):
        url = baseurl + carmodelurl
        print('trying to find url: ' + url)
        page = requests.get(url,headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        for carmodelurl in soup.find_all(html_element_is_car_trim):
            print('we found matching divs')
            trimtowrite = ''
            for child in carmodelurl.children:
                print('this is a child')
                if trimtowrite != '':
                    trimtowrite+=','
                trimtowrite+=child.contents
            if trimtowrite != '':
                dbservice.writetodb(trimsfile,trimtowrite)

dbservice.initialize('text')
#populate_car_model_url_list()
populate_car_models_and_trims()
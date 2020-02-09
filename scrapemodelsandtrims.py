import requests
import dbservice
from bs4 import BeautifulSoup
import re
import json

baseurl = 'https://www.edmunds.com'
modelurls = 'modelurls'
modeltrims = 'modeltrims'
carbrands = 'carbrands'
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
    for carbrand in dbservice.read(carbrands):
        url = baseurl + '/' + carbrand + '/'
        page = requests.get(url,headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        for carmodelurl in soup.find_all(html_element_is_car_model_url):
            dbservice.write(modelurls,carmodelurl.get('href'))

def populate_car_models_and_trims():
    for carmodelurl in dbservice.read(modelurls):
        url = baseurl + carmodelurl
        print('trying to find url: ' + url)
        page = requests.get(url,headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        cleanedsoup = str(soup)
        cleanedsoup = cleanedsoup.replace("\\n","")
        cleanedsoup = cleanedsoup.replace("\\","")
        cleanedsoup = cleanedsoup.replace("  ","")
        cartrims = re.search('"trimInfo": {(.+?)}, "vehicle"',cleanedsoup)
        if cartrims:
            print('found trims for this url')
            jsonfromcartrims = cartrims.group(1)
            jsonfromcartrims = '{'+jsonfromcartrims
            jsonfromcartrims = jsonfromcartrims+'}'
            jsonData = json.loads(jsonfromcartrims)
            for key in jsonData:
                carmodelurlsplit = carmodelurl.split('/')
                datatosave = '{"make": "'+carmodelurlsplit[1]+'", "model": "'+carmodelurlsplit[2]+'", "year": "'+carmodelurlsplit[3]+'", "trim": "'+str(key)+'"'
                subkeys = json.loads(str(jsonData[key]).replace('\'','"'))
                for subkey in subkeys:
                    datatosave += ', "'+str(subkey)+'": "'+str(subkeys[subkey]).replace('\'','"')+'"'
                datatosave += '}'
                dbservice.write(modeltrims,datatosave)

dbservice.initialize('text')
#populate_car_model_url_list()
populate_car_models_and_trims()
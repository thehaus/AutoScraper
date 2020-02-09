import requests
from bs4 import BeautifulSoup
import re
import dbservice
import json

def has_class_but_no_id(tag):
    return tag.has_attr('class')

url = 'https://www.edmunds.com/audi/q7/2019/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
page = requests.get(url,headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
cleanedsoup = str(soup)
cleanedsoup = cleanedsoup.replace("\\n","")
cleanedsoup = cleanedsoup.replace("\\","")
cleanedsoup = cleanedsoup.replace("  ","")
dbservice.write('testaudifile',cleanedsoup)
cartrims = re.search('"trimInfo": {(.+?)}, "vehicle"',cleanedsoup)
if cartrims:
    print('found trims')
    jsonfromcartrims = cartrims.group(1)
    jsonfromcartrims = '{'+jsonfromcartrims
    jsonfromcartrims = jsonfromcartrims+'}'
    jsonData = json.loads(jsonfromcartrims)
    for key in jsonData:
        datatosave = '{"make": "'+'Acura'+'", "model": "'+'TLX'+'", "trim": "'+str(key)+'"'
        subkeys = json.loads(str(jsonData[key]).replace('\'','"'))
        for subkey in subkeys:
            datatosave += ', "'+str(subkey)+'": "'+str(subkeys[subkey]).replace('\'','"')+'"'
        datatosave += '}'
        dbservice.write('testtextfile2',datatosave)
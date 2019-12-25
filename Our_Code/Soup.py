# -*- coding: utf-8 -*-
import csv

import urllib3, re, string, json, html
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib3.exceptions import HTTPError
from io import StringIO

def tag_visible(self, element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def loadAddress(self, address):
    self.locToGet = address
    self.haveHeadline = False
    htmatch = re.compile('.*http.*')
    user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3;rv:36.0) Gecko/20100101 Firefox/36.0'}
    #ps = PorterStemmer() 
    if(htmatch.match(self.locToGet) is None):
        self.locToGet = "http://" + self.locToGet
        if(len(self.locToGet) > 5):
            if(self.msgOutput):
        print("Ready to load page data for: " + self.locToGet +  
               "which was derived from " + address)
        try:
            urllib3.disable_warnings(
                 urllib3.exceptions.InsecureRequestWarning)
            http = urllib3.PoolManager(2, headers=user_agent)
            r = http.request('GET', self.locToGet)
            self.pageData = r.data
            if(self.msgOutput):
                print("Page data loaded OK")
        except:
            self.errMsg = 'Error on HTTP request'
            if(self.msgOutput):
                print("Problem loading the page")
            return False
    self.extractText = ''
    self.recHeadline = self.locToGet
    self.soup = BeautifulSoup(self.pageData, 'html.parser')
    ttexts = self.soup.findAll(text=True)
    viz_text = filter(self.tag_visible, ttexts)
 allVisText = u””.join(t.strip() for t in viz_text)
 for word in allVisText.split():
    canonWord = word.lower()
    canonWord = canonWord.translate(
         str.maketrans(‘’, ‘’, string.punctuation))
    canonWord = canonWord.strip(string.punctuation)
    if(canonWord in self.englishDictionary):
       canonWord = ps.stem(canonWord)
       self.extractText = self.extractText + canonWord + “ “
 
 return True
#url = 'https://www.prothomalo.com/sports/article/1623938/%E0%A6%AC%E0%A6%BE%E0%A6%82%E0%A6%B2%E0%A6%BE%E0%A6%A6%E0%A7%87%E0%A6%B6%E0%A6%95%E0%A7%87-%E0%A6%A8%E0%A6%BF%E0%A7%9F%E0%A7%87-%E0%A6%AF%E0%A7%87-%E0%A6%95%E0%A6%A5%E0%A6%BE%E0%A6%9F%E0%A6%BE-%E0%A6%AC%E0%A6%BE%E0%A6%B0%E0%A6%AC%E0%A6%BE%E0%A6%B0-%E0%A6%AC%E0%A6%B2%E0%A6%B2%E0%A7%87%E0%A6%A8-%E0%A6%B0%E0%A6%BE%E0%A6%B9%E0%A6%BE%E0%A6%A8%E0%A7%87?fbclid=IwAR3hL6YR9AxIS3XUcMRxsbRTanMd7MFee5L703c90eNkJIZ1i386xWNTlk8&h=AT1I28nZvth7y3kdJ3PhKpBbeAHVkNsWIMEFBTtotyNAYxOPc-wWoow4L2w3En0XeL32TAfuUctyxyanui37hXvz6TyMpXKZGzB8sWbMMGXrVlW2qyIAi5YUt-xVFORob3IjGkFg4T8byl1iV5SMGObS8ujGuML_945vdGiyWhkENROF9P4scMT_SyqIFU3EHbeh_xysKqicouF7UBn-B1kNqqqH4CRiZRgyTpUC2VE2R9p9r6O1452baKhnUFcpiuNZM3xFwQOcGubU2AN6v3i6cshzkymu_-9-jNz6ZRlnI7lwVQnHccCAfIC1NrCsTUEozFXv3x2bINUMvWvIWSnJ0bQu3cEMZEx44vZjeIuGnpRG_fYY4G2i2naMSZ2Jz5Ur50ES85KPRQsogVRiFiU4idP1sRYGwWCVNs7Ii-ULaTKrZ5p-xf-FkEjsy-DHbuOGWQ44jpRUnQVqk5ZXUB1_HovyOXfVOd7R5OOOi3AA-aQUShVu-CTiUv7YMnyStJDIsRlE7hi0WaoEU1QTCo9NCqDbRX5BfYLvuPfXhdb22dfyHPnS2r-ECVpJ-eNgKujh4r2dJSC5bfQjTJZ_Yo6HaGpVi7qwgNOrJb9gTIOF4CbwPW6WTb7vs-wAnw9QE3Of'


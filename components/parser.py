from bs4 import BeautifulSoup
import requests
import json
import re
import time
import os
from threading import Thread
import pandas as pd

domin = ['https://la-torta.ua']

def getReviews (bs):
    try:
        return {
            "rating": bs.find('meta', itemprop='ratingValue')['content'],
            "comments": [t.text.replace('\n', '') for t in bs.find_all('div', 'p-review__content') ]
        }
    except:
        return []

def getDelPayIndevid(bs):
    try:
        deliv = bs.find('div', {"data-content-id":'dostavka-4'}).find_all('li')
        pay =  bs.find('div', {"data-content-id":'oplata-4'}).find_all('li')
        return {
                "delivery_methods": [ (t.text.replace('\xa0', ' ').replace('\n', ' ') ) for t in deliv],
                "payment_methods": [ (t.text.replace('\xa0', ' ').replace('\n', ' ') ) for t in pay]
            }
    except:
        return { "delivery_methods": [ ], "payment_methods": []}

def createContent(bs):
    resultProd = None
    pTitle = bs.find('h1', 'product-title')
    desc = bs.find('div', 'product-description')
    img = bs.find('img', 'gallery__photo-img')
    avail = bs.find('div', 'product-header__availability')
    cat = bs.find_all('div', 'breadcrumbs-i')
    price = bs.find('div', 'product-price')
    if ((pTitle!=None) and (desc!=None) and (img!=None) and (avail!=None) and (price!=None) and (cat!=None)):
        try:
            resultProd ={
                "name": pTitle.text,
                "description": desc.text.replace('\n', ' ').replace('\xa0', ' '),
                "price": price.text.replace('\n', "").replace(' ',''),
                "available": True if avail.text.replace(' ', "").replace('\n', '')  == "Вналичии" else False,
                "image": domin[0] + img['src'],
                "categories":[t.text.replace('\n', "") + " " for t in cat[1:]],
                "url":'',
                "reviews": getReviews(bs), 
                "delivery_payment_info": getDelPayIndevid(bs)
            }
        except:
            print("exp")
    return resultProd

# url = 'https://la-torta.ua/termometr-dlya-karameli-i-frityura-1/'
# # url = 'https://la-torta.ua/agar-agar-900gsm2-100gr/'
# bs = BeautifulSoup(requests.get(url).text,"lxml")
# RA = createContent(bs)
# print(RA)

def getDelivery_payment_info():
    bs = BeautifulSoup(requests.get('https://la-torta.ua/shipping-and-payment/').text,"lxml")
    return str(bs.find('section', 'page'))

def getContacts():
    bs = BeautifulSoup(requests.get('https://la-torta.ua/contacts/').text,"lxml")
    return {"addresses": bs.find('span', itemprop='streetAddress').text[:-1].split('\r\n'),
            "phones": [' '.join(t.text.replace('\n', "").split()) for t in bs.find_all('div', 'contacts-info__item--tel')],
            "email": bs.find('a', itemprop='email').text.replace('\n', ''),
            "all_Contacts": str(bs.find('div', 'contacts-text'))
            }
# print(getContacts())

def getSpecial_offers():
    bs = BeautifulSoup(requests.get('https://la-torta.ua/sale/').text,"lxml")
    return  [' '.join(i.text.replace('\n', "").split()) for i in bs.find_all('div', 'catalogCard-title')]
# print(getSpecial_offers())

def GenereteResultFile(numOfTreads, rootPath):
    allProducts = []
    for i in range(numOfTreads):
        f = open(f'{rootPath}sw_templates{i}.json', mode='r', encoding="utf8")
        templates = f.readline().split('},{"name":')
        for i in range(len(templates)-1):
            try:
                allProducts.append(json.loads(str('{"name":' + templates[i]+'}')))
            except:
                allProducts.append(json.loads(str(templates[i]+'}')))
        f.close()

    ResultFile = open(f'{rootPath}ResultFile.json', 'w', encoding='utf-8') 
    json.dump( { 
        "products": allProducts,
        "delivery_payment_info": getDelivery_payment_info(), 
        "contact_info": getContacts(), 
        "special_offers": getSpecial_offers()
        }, ResultFile, ensure_ascii=False)
    ResultFile.close()
# GenereteResultFile(8, '')

def ValidAdress(adr, visit):
    if not (adr in visit):
        if (adr.find('/ua/') == -1) and (len(adr)>1) and (adr.find('siteindex') == -1):
            if (adr.find('/filter/') == -1) or ((adr.find('/filter/') != -1) and (adr.find('/page') != -1) ):
                return True
    return False

def getLinks(url, visited, readyLinks, file):
    url = domin[0] + url
    newLinks = []
    bs = BeautifulSoup(requests.get(url).text,"lxml")
    links = bs.find_all('a', href=(True and re.compile(r'^/')))
    result = createContent(bs)
    if result != None:
        result['url'] = url
        json.dump(result, file, ensure_ascii=False)
        file.write(',')
    for a in links:
        if ValidAdress(a['href'], visited):
            visited.append(a['href'])
            newLinks.append(a['href'])
            readyLinks.append(domin[0] + a['href'])  
    return visited, newLinks, readyLinks

def getRecurseLink(links, visited, readyLinks, file):
    for link in links:
        visited, newLinks, readyLinks = getLinks(link, visited, readyLinks, file)
        if (len(newLinks)>0):
            #print(f'tmpDomain:{link} (len:{len(newLinks)})')
            visited, readyLinks =  getRecurseLink(newLinks, visited, readyLinks, file)
    return visited, readyLinks


def funcForTreadSettings (sz):
    numOfTreads = os.cpu_count()
    if (numOfTreads>=8):
        numOfTreads = numOfTreads - 4 #-4
    elif (numOfTreads>=4):
        numOfTreads = numOfTreads - 2
    else:
        numOfTreads = 1
    
    sizeOneThread = sz // numOfTreads
    ostatok = sz %numOfTreads
    return numOfTreads, sizeOneThread, ostatok

def Main (rootPath):
    f = open(f'{rootPath}sw_templates.json', 'w', encoding='utf-8')
    Visited, nl, ResultLinks = getLinks('', [], [], f)
    numOfTreads, sizeOneThread, ostatok = funcForTreadSettings(len(nl))
    print(f"Number of CPUs which will be used: {numOfTreads} from {os.cpu_count()}")
    print(f'sz:{sizeOneThread} ostatoc:{ostatok}')
    Result = [[] for _ in range(numOfTreads)]
    Files = [open(f'{rootPath}sw_templates{i}.json', 'w', encoding='utf-8') for i in range(numOfTreads)]
    Files.append(f)
    
    def funcForTread(id, start, end, visited, links):
        FinalResult = []
        coun = 0
        for i in range(start, end):# 2=> end
            t1 = time.time()
            visited, nl, FinalResult = getLinks(links[i], visited, FinalResult, Files[id])
            print(f"({id}-{coun})")
            if(id==0): print(f"(tread:{id}){links[i]} (len:{len(nl)}) (id:{i})")
            coun+=1
            visited, FinalResult = getRecurseLink(nl, visited, FinalResult, Files[id])
            if(id == 0): print(f"(time:{time.time() - t1})")
        Result[id] = FinalResult

    pulTreads = []
    t1 = time.time()
    for i in range(numOfTreads): #0 => numOfTreads
        tred = Thread(target=funcForTread, args=(i, sizeOneThread*i, sizeOneThread*(i+1), Visited, nl))
        pulTreads.append(tred)
    [t.start() for t in pulTreads]
    for i in range(len(pulTreads)):
        pulTreads[i].join() 
        print(f"finish:{i}")
        print(len(Result[i]))
        ResultLinks = ResultLinks + Result[i]

    funcForTread(numOfTreads-1, sizeOneThread*(numOfTreads), len(nl), Visited, nl)
    ResultLinks = ResultLinks + Result[numOfTreads-1]

    for i in range(len(Files)):
        Files[i].close()
    
    GenereteResultFile(numOfTreads, rootPath)
    data = pd.DataFrame(ResultLinks)
    data.to_csv(f'{rootPath}all_links.csv')        
    print('Total Time:',time.time() - t1)
    return ResultLinks

# Main('../data/TmpResult')




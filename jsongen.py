#!/usr/bin/env python

# scp webcheck.py md1frejo@ssh.pythonanywhere.com:webmalist

from urllib.request import urlopen
from urllib.parse import urlencode
from IPython.core.debugger import Pdb
from pdb import set_trace as B
from numpy import array,zeros,save,load,dot
from numpy.linalg import norm as norm2
from requests import get
from datetime import datetime
from datetime import date as dt
from urllib.parse import urljoin
import json as js

from json import loads
import requests as req
from selenium import webdriver as we
import re
import yfinance as yf
from bs4 import BeautifulSoup as bs
import pandas as pd

def getstocks():
    # get all stocks from a copied list from  avanza
    # get also omx30
    # duplicate version, latest has the original version
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "DNT": "1",  # Do Not Track
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*looptcp.awk*;q=0.8"
    }

    r1=re.compile(r'company',re.I)
    r2=re.compile(r'\d{1,2}.\d{1,2}')

    avstocks=[]
    omx30={}
    
    url='https://en.wikipedia.org/wiki/OMX_Stockholm_30'
    res=get(url,headers=headers)
    sp=bs(res.content,"html.parser")

    for k in sp.find_all('table',class_=True):
        if r1.search(k.text,re.I):
            ht=k.unwrap
            for l in k.find_all('a',href=True):
                if not l.string=='GICS':
                    li=list(l.next_elements)[:10]
                    key=l.text
                    omx30[key]=[]
                    omx30[key].append(li[3].string.strip())
                    omx30[key].append(li[6].string.strip())
                    b=list(li)[:10][9].string
                    if b:
                        b=r2.search(b)
                    if b:
                        omx30[key].append(b.group())
                    else:
                        omx30[key].append(None)

    with open('astocks.txt','r') as fs:
        asv=fs.readlines()
        
    for l in asv:
        if len(l)>3:
            st=l.strip()
            st=re.sub(r'\s[A|B]','',st)
            avstocks.append(st)

    avstocks=list(set(avstocks))
    
    return omx30,avstocks

def genjson(omx30,url='https://www.affarsvarlden.se/aktie'):

    timed=datetime.today().strftime("%Y-%m-%d %H:%M")
    
    news={}
    news=[]
    news.append({'reccorded':timed})
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "DNT": "1",  # Do Not Track
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*looptcp.awk*;q=0.8"
    }

    url=['https://www.di.se/live',
         'https://www.affarsvarlden.se/aktie',
         'https://www.dn.se',
         'https://www.privataaffarer.se',
         'https://www.svd.se',
         'https://newsoresund.se',
         'https://www.realtid.se',
         'https://www.fastighetsvarlden.se/',
         'https://www.aktiespararna.se/nyheter',
         'https://www.borskollen.se/borsen-idag',
         'https://www.dagensps.se/bors-finans/',
         'https://www.placera.se/telegram']

    res=[get(k,headers=headers) for k in url]
    sp=[bs(k.content,"html.parser") for k in res]
    np=['di','av','pa','svd','dn','on','rt','fv','as','bk','ps','pl']
    attr=['a','p','h1', 'h2','h3','h4','h5']
    
#    res=get(url,headers=headers)
#    sp=bs(res.content,"html.parser")

    for d,f in zip(np,sp):
        for i,k in enumerate(f.find_all(attr)):
            if k.has_attr('class') or k.has_attr('href') or k.has_attr('span'):
                hurl=k.find('a')
                headl=k.text.strip()
                if hurl:
                    hurl=hurl['href']
                else:
                    hurl='missing'
                for l in omx30:
                    stock=l.split()[0]
                    if stock in headl:
                        news.append({'id':i,'headline':headl,'stock':stock,'news':d,'link':hurl})
                        
    with open('news.json','w') as json_file:
        js.dump(news,json_file)

    return news

def gethistory(cand,af='2024-01-01'):

        # provide ticker name, ex: SKF-A.ST and get ticker hist

    hdata=[]
    bf=datetime.now().strftime("%Y-%m-%d")

    with open('./public/conv.json','r') as file:
        conv=js.load(file)

    convk=conv.keys()
    
    for k in cand:
        for l in convk:
            ks=k.upper()
            ls=l.upper().split()
            if ks in ls:
                mname=conv[l]
                res=yf.download(mname,af,bf)
                if res.empty:
                    data={k:"nodata"}
                else:
                    closing_prices=res["Close",mname].tolist()
                    data={k: closing_prices}
                    hdata.append(data)
                    break

    with open("public/ticks.json","w") as f:
        js.dump(hdata,f)

    return hdata

def selectcand(news,tresh):

    stats={}
    
    for l in news[1:]:
        key=l['stock']
        if key in stats.keys():
            stats[key]+=1
        else:
            stats[key]=1

    cand=[l[0] for l in stats.items() if l[1]>tresh]

    return cand
            
def main():

    # get all stocknames
    omx30,avstocks=getstocks()
    news=genjson(omx30)
    # selct candidates with a threshold of 10
    cand=selectcand(news,10)
    hdata=gethistory(cand)
    
    return hdata

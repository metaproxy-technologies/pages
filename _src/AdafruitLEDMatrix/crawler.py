#!/usr/bin/env python
# -*- encoding:utf8 -*-
#Copyright (c) 2017 Tomohiko Araki
#Released under the MIT license
#http://opensource.org/licenses/mit-license.php

import datetime
import time
import argparse
import sys
import os
import random
import feedparser
import hashlib
from glob import glob
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import urllib2
from bs4 import BeautifulSoup
#load Logger
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

def isOkToCrawl():
    crawl_interval = 60 #sec.
    crawl_interval_file = "./lastcrawl"
    now = time.time()

    if os.path.isfile(crawl_interval_file):
        if os.stat(crawl_interval_file).st_mtime > now - 60:
            return False
    
    f = open(crawl_interval_file, 'w')
    f.write(str(now) + "\n")
    f.close()
    return True

def getImageFromFile(path):
    image = Image.open(path).convert('RGB')
    return image

def saveImgFromText(text, imgdir, fontsize):
    path = os.path.abspath(os.path.dirname(__file__))
    if fontsize == 8:
        font   = [ImageFont.truetype(path + '/font/misaki_gothic.ttf', fontsize),1]
    else:
        fontsize = 16
        font  = [ImageFont.truetype(path + '/font/mplus-2c-medium.ttf', fontsize),-2]
        #font  = [ImageFont.truetype(path + '/font/Makinas-Scrap-5.otf', fontsize),-2]
        #font  = [ImageFont.truetype(path + '/font/PixelMplus10-Regular.ttf', fontsize),1]

    color  = [(255,0,255),
             (0,255,255),
             (255,255,0),
             (0,255,0),
             (255,255,255)]

    width, ignore = font[0].getsize(text)
    im = Image.new("RGB", (width + 30, fontsize), "black")
    draw = ImageDraw.Draw(im)
    draw.text((0, font[1]), text, random.choice(color), font=font[0])
    imgname = imgdir+"/"+str(fontsize)+str(hashlib.md5(text.encode('utf_8')).hexdigest())+".ppm"
    if not os.path.exists(imgname):
        im.save(imgname)

def removeOldImg(imgdir):
    #remove ppm files more than 1 days before.
    if not(imgdir=="") and not(imgdir=="/")and not(imgdir=="."): 
        now = time.time()
        for f in os.listdir(imgdir):
            if f[-4:] == '.ppm':
                f = os.path.join(imgdir, f)
                if os.stat(f).st_mtime < now - 0.5 * 86400:
                    if os.path.isfile(f):
                        os.remove(f)

def getNewsFromFeed():
    news  = []
    url = ['https://news.yahoo.co.jp/pickup/economy/rss.xml']
    for tg in url:
        fd = feedparser.parse(tg)
        for ent in fd.entries:
            news.append(u"　　　　　　　　　　"+unicode(ent.title))
    return news

def getNewsFromNikkei():
    news  = []
    url = ['http://www.nikkei.com/',
            'http://www.nikkei.com/news/category/?at=ALL&bn=1',
            'http://www.nikkei.com/news/category/?bn=21']
    for tg in url:
        html = urllib2.urlopen(tg)
        soup = BeautifulSoup(html, "html.parser")
        tags = soup.find_all("span", class_="cmnc-large")
        for tag in tags:
            news.append(u"　　　　　　　　　　"+tag.text)
        tags = soup.find_all("span", class_="cmnc-middle")
        for tag in tags:
            news.append(u"　　　　　　　　　　"+tag.text)
        tags = soup.find_all("span", class_="cmnc-small")
        for tag in tags:
            news.append(u"　　　　　　　　　　"+tag.text)
        tags = soup.find_all("span", class_="cmnc-xsmall")
        for tag in tags:
            news.append(u"　　　　　　　　　　"+tag.text)
        time.sleep(2.0)
        
    return news

parser = argparse.ArgumentParser()
#parser.add_argument("-r", "--led-rows", action="store", help="Display rows. 16 for 16x32, 32 for 32x32. Default: 32", default=16, type=int)

if isOkToCrawl():
    print ("I gonna crawl.")
    
    imgdir = os.path.abspath(os.path.dirname(__file__)) + "/newsimg"
    if not os.path.isdir(imgdir):
        os.mkdir(imgdir)

    #clean up old news
    removeOldImg(imgdir)

    #get from RSS feed
    for text in getNewsFromFeed():
        saveImgFromText(text, imgdir, 8)

    #get from Nikkei
    for text in getNewsFromNikkei():
        saveImgFromText(text, imgdir, 8)

else:
    print ("You need to wait for 1min before next crawl.")



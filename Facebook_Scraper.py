#!/usr/bin/env python
from bs4 import BeautifulSoup,Comment
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import os
import sys
from threading import Thread

def download_parellel(function,images,output):
    for i in images:
        Thread(target=function,args=(i,output,)).start()
    

def download(image,output):
    filename = image.split("/")[-1]
    outpath = os.path.join(output, filename)   
    urlretrieve(image, outpath)
       

def main(url,output):
    links=[];
    soup = BeautifulSoup(urlopen(url))
    parsed = list(urlparse.urlparse(url))
    #print soup
    comments = soup.findAll(text=lambda text:isinstance(text,Comment))
    for comment in comments:
        test = BeautifulSoup(comment)
        nameTags = test.findAll('div',{"data-starred-src":True})
        if nameTags:
            for i in nameTags:
                links.append(i['data-starred-src']);
            
            
    download_parellel(download,links,output)
        
if __name__ == "__main__":
    url = sys.argv[-1]
    output = "/Users/rkarth/"
    main(url, output)
    

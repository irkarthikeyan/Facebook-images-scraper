#!/usr/bin/env python
from bs4 import BeautifulSoup,Comment
import urlparse
from urllib2 import urlopen
import urllib2
from urllib import urlretrieve
import os
import sys
import json
from threading import Thread
import httplib
import requests
import re
def download_parellel(function,images,output):
    for i in images:
        Thread(target=function,args=(i,output,)).start()
    

def download(image,output):
    filename = image.split("/")[-1]
    outpath = os.path.join(output, filename)   
    urlretrieve(image, outpath)
       

def extract_from_ajax(download,output,load_url,last_fbid):
    url = "http://graph.facebook.com/"+load_url
    connect = requests.get(url)
    o = connect.json()
    
    ajaxurl = "https://www.facebook.com/ajax/pagelet/generic.php/TimelinePhotosStreamPagelet?ajaxpipe=1&ajaxpipe_token=AXif26PCkG9XwzHk&no_script_path=1&data=%7B%22scroll_load%22%3Atrue%2C%22last_fbid%22%3A"+last_fbid+"%2C%22fetch_size%22%3A32%2C%22profile_id%22%3A"+o['id']+"%2C%22tab_key%22%3A%22photos_stream%22%2C%22sk%22%3A%22photos_stream%22%7D&__user=0&__a=1&__dyn=7w86i&__req=jsonp_2&__adt=2"
    
    connection = requests.get(ajaxurl)
    
    obj = connection.content
    pattern_one = re.findall("http:\\\\/\\\\/[a-z]+-[a-z]+.[a-z]+.[a-z]+.[a-z]+.\\\\/[a-z]+-[a-z]+-[a-z0-9]+\\\\/[a-z0-9]+\\\\/[0-9]+_[0-9]+_[0-9]+_[a-z]+.jpg",obj)
    pattern_two = re.findall("https:\\\\/\\\\/[a-z]+-[a-z]+-[a-z]+-[a-z]+.[a-z]+.[a-z]+\\\\/[a-z]+-[a-z]+-[a-z0-9]+\\\\/[a-z0-9]+\\\\/[0-9]+_[0-9]+_[0-9]+_[a-z]+.jpg",obj)
    nextLinks = [];
    cnt = 1
    for i in pattern_one:
        link = ""
        for j,c in enumerate(i):
            if c != '\\':
                link = link + c
            
            
        nextLinks.append(link)
        print link
    
    for i in pattern_two:
        link = ""
        for j,c in enumerate(i):
            if c != '\\':
                link = link + c
            
            
        nextLinks.append(link)
        print link    
    
    download_parellel(download,nextLinks,output)
    last_link = nextLinks[-2]
    last_id = last_link.split("_")
    if last_id:
        return last_id[-3]
    return None


def main(url,output,load_url):
    links=[];
    soup = BeautifulSoup(urlopen(url))
    parsed = list(urlparse.urlparse(url))
    #print soup
    comments = soup.findAll(text=lambda text:isinstance(text,Comment))
    for comment in comments:
        #print comment
        #print "\n\n\n"
        test = BeautifulSoup(comment)
        nameTags = test.findAll('div',{"data-starred-src":True})
        lastImage = ""
        if nameTags:
            for i in nameTags:
                links.append(i['data-starred-src'])
                
    download_parellel(download,links,output)
    
    #Ajax loading for further images
    
    lastImage =  links[-2]
    ret = lastImage.split("_");
    lastid = extract_from_ajax(download,output,load_url,ret[-3])
    
    while lastid:
        lastid = extract_from_ajax(download,output,load_url,lastid)
    
    
if __name__ == "__main__":
    url = sys.argv[-1]
    #Change your location
    output = "/Users/rkarth/downloads" 
    all_parts = url.split("/")
    load_url = all_parts[-2]
    main(url, output,load_url)
    

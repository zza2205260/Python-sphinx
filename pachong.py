
# -*- coding:utf-8 -*-  
import urllib2
import json
import re 
import thread
import time

_count = 0
location_array = []
 

 
def city2point(str_city):
    f=urllib2.urlopen("http://api.map.baidu.com/telematics/v3/geocoding?keyWord=%s&cityName=131&out_coord_type=gcj02&ak=lCw7Oh8zDaaSk7VBytVMPiV6NgmxLFAy&output=json"%str_city)
    data = f.read()
    data = eval(data)
    if data['results']['location']['lat'] != '':
        location_array.append(data['results']['location']);
        print location_array
 
   

def gethtml(url):
    time.sleep(5)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    try:
        request = urllib2.Request(url,headers = headers)
        response = urllib2.urlopen(request)
        data = response.read()
        if data:
            return data
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
    return

def analysishtmlpeople(htmlstr):
    pong = re.compile('href="/people/.+?"')
    result = pong.findall(htmlstr)
    p_array = []
    for x in xrange(0,len(result)):
        p_url = result[x].split('"')
        p_array.append(p_url[1]) 
    return p_array

def analysishtmllocation(htmlstr):
    if type(htmlstr) != str:
        return
    pong_location = re.compile('class="location item".+?title="([^"]+?)"')
    pong_name = re.compile('class="position item".+?title="([^"]+?)"')
    try:
        result = pong_location.findall(htmlstr)
        # result_name = pong_name.findall(htmlstr)
        if result:
            for x in xrange(0,len(result)):
                city2point(result[x])        
            # if result_name:
            #     for i in xrange(0,len(result_name)):
            #         print result_name[i] 
    except Exception, e:
        raise e

def go(url,number):
    try:
        htmlstr = gethtml(url)          
        peopleurl = analysishtmlpeople(htmlstr)
        for i in xrange(0,len(peopleurl)):
            location_url = 'https://www.zhihu.com%s'%(peopleurl[i])
            location_html = gethtml(location_url)
            location_str = analysishtmllocation(location_html)
    except Exception, e:
        raise e
    global _count
    _count += 1
    print _count
    
    return 

def writejson(strjosn):
    name = "../python/city.json"
    fo = open(name,"w+")
    fo.write(strjosn)
    fo.close



number = 0
for page in xrange(1,50):
    time.sleep(5)
    url = 'https://www.zhihu.com/topic/19552192/top-answers?page=%d'%(page)
    thread.start_new_thread(go,(url,number,))

raw_input('***********开始*************')




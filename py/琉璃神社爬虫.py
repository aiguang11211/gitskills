#-*- coding=utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',

}

def request(page):
    requests.packages.urllib3.disable_warnings()
    base_url='http://llss.lol/wp/category/all/comic/page/'
    response=requests.get(base_url+str(page)+'/',headers=headers,verify=False)
    if response.status_code==200:
        addr=[]
        data=[]
        name=[]
        req=BeautifulSoup(response.text,'html.parser')
        req1=req.find_all('h1',class_='entry-title')
        req2=BeautifulSoup(str(req1),'html.parser')
        req3=req2.find_all('a')
        for i in req3:
            requests.packages.urllib3.disable_warnings()
            response1 = requests.get(i.get('href'), headers=headers, verify=False)
            req4 = BeautifulSoup(response1.text, 'html.parser')
            req5=req4.find_all('div',class_="entry-content")
            req7 = req4.find_all('h1', class_='entry-title')
            a=re.compile('[A-Za-z0-9]{40}')
            b=re.compile('[A-Za-z0-9]{32}')
            c=re.search(a,str(req5))
            d=re.search(b,str(req5))
            if c:
                print(req7[0].text)
                print(c.group())
                print('c')
                name.append(req7[0].text)
                addr.append('magnet:?xt=urn:btih:' + c.group())
            elif d:
                print(req7[0].text)
                print(d.group())
                print('d')
                name.append(req7[0].text)
                addr.append('magnet:?xt=urn:btih:' + d.group())
        data.append(name)
        data.append(addr)
        return data

def write_to_file(addr,name):
    with open('C:/Users/拉布拉多搭/Desktop/磁力链接.txt','a',encoding='utf-8') as f:
        f.write(name+'\n')
        f.write(addr+'\n')

def main():
    for j in range(10):
        data=request(j+1)
        for i in range(len(data[0])):
            print('正在获取第%d页第%d个链接'%(j+1,i+1))
            write_to_file(data[1][i],data[0][i])
            print('获取完成')

if __name__=='__main__':
    print('开始下载')
    main()
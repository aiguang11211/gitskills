#-*- coding=utf-8 -*-
import requests
from urllib.parse import urlencode


NUMBER_OF_PHONE=100
base_url='https://unsplash.com/napi/photos?'
header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Referer':'https://unsplash.com/',
    'Connection':'keep-alive',
    'Cookie': '_ga=GA1.2.836275500.1541140126; _gid=GA1.2.1915197463.1541140126; uuid=8d5a71c0-de68-11e8-99d0-d5eda177d734; xpos=%7B%7D; lux_uid=154120493972813839; _sp_ses.0295=*; lsnp=9JeXImRHkl4; un_sesh=VGQwTHRLZlE1bk9PL2dadnBQRWtVak1VaU9aREFwMForbXNOSTRTK213MWFDN2hSYkFzeWNqYmlBNC9QM25ybCs0NEJuL0NZcVcrbFZTdG5qa1hxcXNMYTlLRmxkcFpWcG1xVmw4YTBZSElVeU9mV2VGMlZtMjg3SEhOaWNicnJnNDRmcTcrV0ZIQUdzT0ZCSVdDZFdBPT0tLWg5aE9UeWFRNVM0TzQyeU10TEtnZkE9PQ%3D%3D--934068662ae27e036ee23a62ce4efa66ce8bd6c0; _gat=1; _sp_id.0295=c3e064e5-ed84-4632-ac92-bf1d51a00de1.1541140127.2.1541209074.1541140927.64aa7fcc-5c7d-4336-bcbe-c8ebe96c8f8f',
    'Host':'unsplash.com',
    'X-Requested-With':'XMLHttpRequest'}

def json_parse(page):
    parms={
        'page':str(page),
        'per_page':'12',
        'order_by':'latest'
    }
    url=base_url+urlencode(parms)
    requests.packages.urllib3.disable_warnings()
    response=requests.get(url,headers=header,verify=False)
    if response.status_code==200:
        json=response.json()
        photo_url_download_true=[]
        photo_id=[]
        data=[]
        for i in range(len(json)):
            photo_url_id=json[i].get('id')
            photo_url_download='https://unsplash.com/photos/'+photo_url_id+'/download?force=true'
            print(photo_url_download)
            response1=requests.get(photo_url_download,headers=header,verify=False, allow_redirects=False)
            photo_url_download=response1.headers['Location']
            photo_url_download_true.append(photo_url_download)
            photo_id.append(photo_url_id)
        data.append(photo_url_download_true)
        data.append(photo_id)
        return data
    else:print('获取重定向后的url失败')

def write_to_file(photo_url_download_true,id,page,number):
    print(photo_url_download_true)
    response2=requests.get(photo_url_download_true,verify=False)
    print(response2)
    if response2.status_code==200:
        print('200')
        file_path='C:/Users/拉布拉多搭/Desktop/Unsplash/'+id+'.jpg'
        with open(file_path,'wb') as f:
            f.write(response2.content)
        print('正在下载第%d张图片'%(page*11+number+1))
        print(id+'.jpg'+'下载成功')
    else:
        print('下载失败')

def calc():
    page=(NUMBER_OF_PHONE-1)//12  #8
    number=NUMBER_OF_PHONE-page*12  #4
    return [page,number]

def main():
    pages=calc()[0]
    numbers=calc()[1]
    for page in range(pages):
        print('********************请耐心等待********************')
        data = json_parse(page)
        print(data)
        for count in range(12):
            print('enter')
            write_to_file(data[0][count], data[1][count], page, count)
    print("********************请耐心等待********************")
    data = json_parse(pages)
    for number in range(numbers):
        write_to_file(data[0][number], data[1][number], pages, number)

if __name__=='__main__':
    main()

# -*- coding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import sys

'''
http://www.biqukan.cc/在这里找小说
'''


class downloader(object):
    def __init__(self):
        self.target = input('请输入需要下载小说的主页')
        self.names = []  # 章节名
        self.urls = []  # 存放章节链接
        self.nums = 0  # 章节数
        self.title='a'

    def get_download_url(self):
        req = requests.get(self.target)
        html = req.content.decode('gbk')
        div_bf = BeautifulSoup(html, 'html.parser')
        div = div_bf.find_all('div', class_="panel panel-default", id="list-chapterAll")
        a_bf = BeautifulSoup(str(div[0]), 'html.parser')
        a = a_bf.find_all('a')
        self.nums = len(a)
        for each in a:
            self.names.append(each.string)
            self.urls.append(self.target + each.get('href'))
        div1 = div_bf.find_all('h1', class_="bookTitle")
        a_bf1 = BeautifulSoup(str(div1[0]), 'html.parser')
        self.title=a_bf1.text

    def get_contents(self, target):
        req = requests.get(target)
        html = req.content.decode('gbk')
        bf = BeautifulSoup(html, 'html.parser')
        texts = bf.find_all('div', class_="panel-body", id="htmlContent")
        texts = texts[0].text.replace('\xa0*4', ' ')
        return texts

    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


if __name__ == '__main__':
    dl = downloader()
    dl.get_download_url()
    print('《%s》开始下载:'%dl.title)
    for i in range(dl.nums):
        dl.writer(dl.names[i], '%s.txt'%dl.title, dl.get_contents(dl.urls[i]))
        sys.stdout.write('已下载:%.3f%%' % float(i / dl.nums) + '\r')
        sys.stdout.flush()
    print('《%s》下载完成'%dl.title)








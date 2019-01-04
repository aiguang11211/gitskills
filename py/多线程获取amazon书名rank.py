#!/usr/bin/env python
from atexit import register
from re import compile
from time import ctime
from threading import Thread
import requests

header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }

REGEX=compile('#([\d,]+) in Books ')
AMZN='https://www.amazon.com/dp/'
ISBNs={
    '0132269937':'Core Python Programming',
    '0132356139':'Python Web ',
    '0137143419':'Python Fundamentals',
}

def getRanking(isbn):
    page=requests.get('%s%s'%(AMZN,isbn),headers=header)
    print(page.status_code)
    return REGEX.findall(page.text)[0]

def _showRanking(isbn):
    print('- %r ranked %s'%(ISBNs[isbn],getRanking(isbn)))

def main():
    print('At',ctime(),'on Amazon...')
    for isbn in ISBNs:
        Thread(target=_showRanking,args=(isbn,)).start()

@register
def _atexit():
    print('all done at:',ctime())

if __name__=="__main__":
    main()


#!/usr/bin/env python
from atexit import register
from random import randrange
from threading import Thread,Lock,BoundedSemaphore
from time import ctime,sleep

lock=Lock()
MAX=5
candytray=BoundedSemaphore(MAX)

def refill():
    with lock:
        print('Refill candy...')
        try:
            candytray.release()
        except ValueError:
            print('full,skipping')
        else:
            print('OK')

def buy():
    with lock:
        print('Buying candy...')
        if candytray.acquire(False):#不允许阻塞
            print('OK')
        else:
            print('empty,skipping')

def producer(loops):
    for i in range(loops):
        refill()
        sleep(randrange(3))

def consumer(loops):
    for i in range(loops):
        buy()
        sleep(randrange(3))

def main():
    print("starting at:",ctime())
    nloops=randrange(2,6)
    print('THE CANDY MACHINE (FULL with %d bars!)'%MAX)
    Thread(target=consumer,args=(randrange(nloops,nloops+MAX+2,))).start()
    Thread(target=producer,args=(nloops,)).start()

@register
def _atexit():
    print('all done at:%s'%ctime())

if __name__=='__main__':
    main()
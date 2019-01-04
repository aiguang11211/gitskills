#!/usr/bin/env python
from atexit import register
from random import randrange
from threading import Thread,Lock,current_thread
from time import ctime,sleep

class CleanOutputSet(set):
    def __str__(self):
        return ','.join(x for x in self)

lock=Lock()
loops=(randrange(2,5) for x in range(randrange(3,7)))
remaining=CleanOutputSet()

def loop(nsec):
    myname=current_thread().name
    with lock:
        remaining.add(myname)
        print('[{0}] started {1}'.format(myname,ctime()))

    sleep(nsec)
    with lock:
        remaining.remove(myname)
        print('[{0}] completed {1}'.format(myname,ctime()))
        print(' (remianing:{0})'.format(remaining or 'NONE'))

def main():
    for pause in loops:
        Thread(target=loop,args=(pause,)).start()

@register
def _atexit():
    print('all done at:%s'%ctime())

if __name__=='__main__':
    main()
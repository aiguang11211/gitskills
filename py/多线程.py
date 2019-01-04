#！/usr/bin/env python
import threading
from time import ctime,sleep

loops=[4,2]

class MyThread(threading.Thread):
    def __init__(self,func,args,name):
        threading.Thread.__init__(self)
        self.name=name
        print(self.name)
        self.args=args
        self.func=func

    def run(self):
        self.func(*self.args)

def loop(nloop,nsec):
    print('loop %s start at:%s'%(nloop,ctime()))
    sleep(nsec)
    print('loop %s over at %s'%(nloop,ctime()))

def main():
    print("project start at ",ctime())
    threads=[]
    nloops=range(len(loops))
    for i in nloops:
        t=MyThread(loop,(i,loops[i]),loop.__name__)
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print("project over at ",ctime())

if __name__=='__main__':
    main()
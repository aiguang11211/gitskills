#!usr/bin/env python
from time import ctime
from string import ascii_lowercase as lc
from random import randrange,choice
from sys import maxsize

tlds=('com','edu','net','org','gov')

for i in range(randrange(5,11)):
    dtint=randrange(maxsize)%10000000000
    dtstr=ctime(dtint)
    llen=randrange(4,8)
    login=''.join(choice(lc) for j in range(llen))
    dlen=randrange(llen,13)
    dom=''.join(choice(lc) for j in range(dlen))
    print('%s::%s@%s.%s::%d-%d-%d'%(dtstr,login,dom,choice(tlds),dtint,llen,dlen))
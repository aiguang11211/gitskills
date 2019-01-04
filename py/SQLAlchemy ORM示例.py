#!usr/bin/env python

from os.path import dirname
from random import randrange as rand
from sqlalchemy import Column,Integer,String,create_engine,orm
from sqlalchemy.ext.declarative import declarative_base
DBNAME='test'
NAMELEN=16
COLSIZ=10
RDBMSs={'s':'sqlite','m':'mysql'}
FIELDS=('login','userid','projid')
NAMES=(
    ('aaron',8312),('asda',3233),('dasfzs',2332),
)
tformat=lambda s:str(s).title().ljust(COLSIZ)
cformat=lambda s:s.upper().ljust(COLSIZ)

DSNs={
    'mysql':'mysql+mysqlconnector://root:aiguang11211@localhost/%s'%DBNAME,
    'sqlite':'sqlite:///:memory:',
}

Base=declarative_base()

def randName():
    pick=set(NAMES)
    while pick:
        yield pick.pop()

def setup():
    return RDBMSs[input('''
    Choose a database system:
    
    (M)ySQL
    (S)QLite
    
    Enter choice: ''').strip().lower()[0]]

class Users(Base):
    __tablename__='users'
    login=Column(String(NAMELEN))
    userid=Column(Integer,primary_key=True)
    projid=Column(Integer)
    def __str__(self):
        return ''.join(map(tformat,(self.login,self.userid,self.projid)))

class SQLAlchemyTest(object):
    def __init__(self,dsn):
        try:
            eng=create_engine(dsn)

        except ImportError:
            raise RuntimeError()
        try:
            eng.connect()
        except Exception:
            eng=create_engine(dirname(dsn))
            eng.execute('CREATE DATABASE %s'%DBNAME).close()
            eng = create_engine(dsn)

        Session=orm.sessionmaker(bind=eng)
        self.ses=Session()
        self.users=Users.__table__
        self.eng=self.users.metadata.bind=eng

    def insert(self):
        self.ses.add_all(
            Users(login=who,userid=userid,projid=rand(1,5)) \
            for who,userid in randName()
        )
        self.ses.commit()

    def dbDump(self):
        print('\n%s'%''.join(map(cformat,FIELDS)))
        users=self.ses.query(Users).all()
        for user in users:
            print(user)
        self.ses.commit()

    def update(self):
        fr=rand(1,5)
        to=rand(1,5)
        i=-1
        users=self.ses.query(Users).filter_by(projid=fr).all()
        for i,user in enumerate(users):
            user.projid=to
        return fr,to,i+1

    def delete(self):
        rm=rand(1,5)
        i=-1
        users=self.ses.query(Users).filter_by(projid=rm).all()
        for i,user in enumerate(users):
            self.ses.delete(user)
        return rm,i+1

    def __getattr__(self,attr):
        return getattr(self.users,attr)

    def finish(self):
        self.ses.connection().close()

def main():
    print('***Connect to %s database'%DBNAME)

    db=setup()
    if db not in DSNs:
        print('\nERROR:%s not supported,exit'%db)
        return
    try:
        orm=SQLAlchemyTest(DSNs[db])
    except RuntimeError:
        print('\nERROR:%s not supported,exit'%db)
        return

    print('\n*** Create users table （drop old one if appl.）')
    orm.drop(checkfirst=True)
    orm.create()

    print('\n *** Insert names into table')
    orm.insert()
    orm.dbDump()

    print('\n *** Move users to a random group')
    fr,to,num =orm.update()
    print('\t(%d users moved) from (%d) to (%d)'%(num,fr,to))
    orm.dbDump()

    print('\n*** Randomly delete group')
    rm,num=orm.delete()
    print('\t(group #%d;%d users removed)'%(rm,num))
    orm.dbDump()

    print('\n*** Drop users table')
    orm.drop()
    print('\n*** Close cxns')
    orm.finish()

if __name__=='__main__':
    main()

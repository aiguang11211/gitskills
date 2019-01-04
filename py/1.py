#database.py
import sys,shelve

def store_person(db):
        """
        store
        """
        pid=input("Enter unique ID number:")
        person={}
        person['name']=input('Enter name:')
        person['age']=input('Enter age:')
        person['phone']=input('Enter phone:')

        db[pid]=person

def lookup_person(db):
        """
        lookup
        """
        pid=input('Enter ID number:')
        field=input("What would you like to know?<name,age,phone>")
        field=field.strip().lower()
        print(field.capitalize()+':'+db[pid][field])

def print_help():
        print("The available commands are:")
        print("store:")

def enter_command():
        cmd=input("Enter command(? for help)")
        cmd=cmd.strip().lower()
        return cmd

def main():
        database=shelve.open('C:\\Users\\拉布拉多搭\\Desktop\\py\\database.dat')
        try:
                while True:
                        cmd=enter_command()
                        if cmd=='store':
                                store_person(database)
                        elif cmd=='lookup':
                                lookup_person(database)
                        elif cmd=='?':
                                print_help()
                        elif cmd=='quit':
                                return
        finally:
                database.close()

if __name__=='__main__':main()

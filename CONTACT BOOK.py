import mysql.connector as con
db=con.connect(host="localhost", user="root", password="sql2005")
dbcur=db.cursor()
def setup():
    db="""create database if not exists CONTACT"""
    dbcur.execute(db)
    use="""use CONTACT"""
    dbcur.execute(use)
    tab1="""create table if not exists BOOK (SNO bigint(100) primary key, Name Varchar(1000), NUMBERS BIGINT(11) NOT NULL )"""
    dbcur.execute(tab1)
def adder():
    while True:
        print("_" * 100)
        print("ADDER")
        print("_" * 100)
        use = """use CONTACT"""
        dbcur.execute(use)
        tab7 = """select SNO from BOOK"""
        dbcur.execute(tab7)
        show3 = dbcur.fetchall()
        if show3 == []:
            i = 1
        else:
            C = len(show3)
            i = C + 1
        A=input("Enter the name=")
        B=int(input("Enter the number "))
        tab2="""insert into BOOK VALUES ({},'{}',{})""".format(i, A,B)
        dbcur.execute(tab2)
        db.commit()
        ch3 = input("wish to continue(Y/N):")
        if ch3 in "Nn":
            break
    Menu()
def shower():
    while True:
        print("_" * 100)
        print("SHOWER")
        print("_" * 100)
        use = """use CONTACT"""
        dbcur.execute(use)
        tab3="""select * from BOOK"""
        dbcur.execute(tab3)
        show1=dbcur.fetchall()
        print("SNO", "NAME", "NUMBERS", end="\t")
        print(show1)
        for i in show1:
            print(i[0],'\t', i[1],'\t', i[2])
        ch3 = input("wish to continue(Y/N):")
        if ch3 in "Nn":
            break
    Menu()
def searcher():
    while True:
        use = """use CONTACT"""
        dbcur.execute(use)
        print("_" * 100)
        print("SEARCHER")
        print("_" * 100)
        global L
        L=[]
        tab4 = """select * from BOOK"""
        dbcur.execute(tab4)
        show2= dbcur.fetchall()
        A=input("Enter the name")
        for i in show2:
            if A in i[1]:
                L.append(i)
        if len(L)==0:
            print("No result")
        else:
            print("Searches are")
            print("SNO", "NAME", "NUMBERS", end="\t")
            for i in L:
                print(i[0],'\t', i[1],'\t', i[2])
        ch3 = input("wish to continue(Y/N):")
        if ch3 in "Nn":
            break
    Menu()
def deleter():
    while True:
        use = """use CONTACT"""
        dbcur.execute(use)
        searcher()
        print("_" * 100)
        print("DELETER")
        print("_" * 100)
        if len(L)!=0:
            print("SELECT SNO OF NUMBER TO DELETE")
            A=int(input("Enter the SNO="))
            for i in L:
                if A==i[0]:
                    tab5="""delete from BOOK where SNO={}""".format(A)
                    dbcur.execute(tab5)
                    db.commit()
        else:
            print("Orperation is not valid")
        ch3 = input("wish to continue(Y/N):")
        if ch3 in "Nn":
            break
    Menu()

def modifier():
    while True:
        use = """use CONTACT"""
        dbcur.execute(use)
        print("_" * 100)
        print("MODIFIER")
        print("_" * 100)
        searcher()
        if len(L)!=0:
            print("SELECT SNO OF NUMBER TO DELETE")
            A=int(input("Enter the SNO="))
            for i in L:
                if A==i[0]:
                    while True:
                        print(L[A])
                        print("press 1 to change the Name")
                        print("press 2 to change the Telephone")
                        print("press 3 to leave")
                        ch1=int(input("Enter the choice="))
                        if ch1==1:
                            B=input("Enter the Name=")
                            tab6="""update Book set Name = '{}' where SNO={}""".format(B,A)
                            dbcur.execute(tab6)
                            db.commit()
                            print("Modification succesful")
                        elif ch1==2:
                            B = input("Enter the Name=")
                            tab6 = """update Book set Name = '{}' where SNO={}""".format(B, A)
                            dbcur.execute(tab6)
                            db.commit()
                            print("Modification succesful")
                        elif ch1==3:
                            break
                        else:
                            print("invalid choice")
        else:
            print("orperation not possible")
        ch3=input("wish to continue(Y/N):")
        if ch3 in "Nn":
            break
    Menu()
def Menu():
    setup()
    while True:
        print("_"*100)
        print("MENU")
        print("_" * 100)
        print("press 1 to enter new contact")
        print("press 2 to enter modify contact")
        print("press 3 to delete contact")
        print("press 4 to search contact")
        print("press 5 to show contact list")
        print("press 6 to exit")
        ch1 = int(input("Enter the choice="))
        if ch1==1:
            adder()
        elif ch1==2:
            modifier()
        elif ch1==3:
            shower()
        elif ch1==4:
            deleter()
        elif ch1==5:
            shower()
        elif ch1==6:
            print("Thanks for using")
            break
        else:
            print("invalid choice")
Menu()





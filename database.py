import sqlite3 as sql
from xmlrpc.client import boolean

def Create_User(Username,Password):
    db = sql.connect("test.db")
    
    sql2 = ''' INSERT INTO USERS(Username,Password)
              VALUES(?,?) '''
    db.execute(sql2, (Username,Password))
    db.commit()
    db.close()

def Get_User(Username,Password) -> bool:
    db = sql.connect("test.db")
    
    n = db.execute("SELECT * from USERS WHERE Username = (?) and Password = (?)",(Username,Password))
    if n.fetchall() == []:
        return False
    
    db.close()

    return True

# def b():
#     conn = sql.connect('test.db')

#     cursor = conn.execute("SELECT * from USERS")
#     for row in cursor:
#         print ("ID = ", row[0])
#         print ("NAME = ", row[1])

#     conn.close()



# Create_User("admin","admin123")
# b()
# print(Get_User("admin","admin123"))

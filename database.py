import sqlite3 as sql

# def create_Table():
#     con = sql.connect("test.db")
#     cur = con.cursor()
#     qurey = ''' CREATE TABLE Files
#                 ( UName     varchar (255) not null,
#                   File varchar(128) NOT NULL,
#                   Sent_by varchar(255) NOt NULL,
#                   FOREIGN KEY(UName) REFERENCES  USERS (Username)
#                   );'''
                  
#     con.execute(qurey)
#     con.commit()

#     con.close()

def get_File_count(Username):
    db = sql.connect("test.db")

    conut = db.execute(
        "SELECT COUNT(File) from Files WHERE Uname = (?) ", (Username,))
    conut = conut.fetchall()
    if len(conut) == 0:
        return 0

    db.close()
    COUNT = conut[0]
    return COUNT [0]
    
    
    
    
def Create_User(Username, Password) -> bool:
    db = sql.connect("test.db")

    try:
        db.execute("INSERT INTO USERS(Username,Password) VALUES(?,?) ", (Username, Password))
        db.commit()
        db.close()
        return True
    except sql.IntegrityError:
        return False

def add_public_key(Username, Key) -> bool:
    db = sql.connect("test.db")

    try:
        db.execute("INSERT INTO Public_Keys(Uname,Public_Key) VALUES(?,?) ", (Username, Key))
        db.commit()
        db.close()
        return True
    except sql.IntegrityError:
        return False


def Get_User(Username, Password) -> bool:
    db = sql.connect("test.db")

    User = db.execute(
        "SELECT * from USERS WHERE Username = (?) and Password = (?)", (Username, Password))

    if len(User.fetchall()) == 0:
        return False

    db.close()

    return True

def get_public_key(Username):
    db = sql.connect("test.db")

    key = db.execute(
        "SELECT Public_key from Public_Keys WHERE Uname = (?) ", (Username,))
    key = key.fetchall()
    if len(key) == 0:
        return False

    db.close()
    KEY = key[0]
    return KEY [0]
    
def add_File(Username, File,Sender) -> bool:
    db = sql.connect("test.db")

    try:
        db.execute("INSERT INTO Files(UName,File,Sent_by) VALUES(?,?,?) ", (Username, File,Sender))
        db.commit()
        db.close()
        return True
    except sql.IntegrityError:
        return False

def get_File(Username):
    db = sql.connect("test.db")

    File = db.execute(
        "SELECT File from Files WHERE UName = (?) ", (Username,))
    File = File.fetchall()
    if len(File) == 0:
        return False

    db.close()
    FILE = File
    files =""
    for x in range(len(FILE)):

        files +="+"+ FILE[x][0] 
    return files
    
def get_all():
    conn = sql.connect('test.db')

    cursor = conn.execute("SELECT * from Files")
    for row in cursor:
        print("Username = ", row[0])
        print("Password = ", row[1], '\n')
        print("Password = ", row[2], '\n')

    conn.close()





# Create_User("admin","admin123")
# b()
# print(Get_User("admin","admin123"))
# create_Table()

# print(add_public_key("admin","aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))
# print(get_public_key("admin"))
# get_all()


# print(add_File("admin","ewewdwedw","abdullah"))
# print(get_File("admin").split('+')[0:])
print(get_File_count("admin"))


import sqlite3 as sql

def create_Table():
    con = sql.connect("test.db")
    cur = con.cursor()
    # qurey = ''' CREATE TABLE Public_Keys
    #             ( UName     varchar (255) not null,
    #               Public_key varchar(255) NOT NULL,
    #               FOREIGN KEY(UName) REFERENCES  USERS (Username)
    #               );'''
    # q = '''
    #         DROP TABLE Public_keys
    #     '''
    qurey = ''' CREATE TABLE Files
                ( name     varchar (255) not null,
                  path     varchar (255) NOT NULL,
                  Sender   varchar (255) NOT NULL,
                  session_key varchar (128) NOT NULL,
                  FOREIGN KEY(name) REFERENCES  USERS (Username)
                  FOREIGN KEY(Sender) REFERENCES  USERS (Username)
                  );'''
    q = '''
            DROP TABLE Files
        '''       
    con.execute(qurey)
    con.commit()

    con.close()

def get_File_count(Username):
    db = sql.connect("test.db")

    conut = db.execute(
        "SELECT COUNT(path) from Files WHERE name = (?) ", (Username,))
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
    return KEY 
    
def add_File(Username, File,Sender,session_key) -> bool:
    db = sql.connect("test.db")

    try:
        db.execute("INSERT INTO Files(name,path,Sender,session_key) VALUES(?,?,?,?) ",
                   (Username, File, Sender, session_key))
        db.commit()
        db.close()
        return True
    except sql.IntegrityError:
        return False

def get_File(Username):
    db = sql.connect("test.db")

    File = db.execute(
        "SELECT path , Sender from Files WHERE name = (?) ", (Username,))
    File = File.fetchall()
    if len(File) == 0:
        return False

    db.close()
    FILE = File
    files =""
    # print(FILE)
    # print(FILE[0][0])
    # # print(FILE[0][1])
    # print(FILE[1][0])
    # # print(FILE[1][1])

    for x in range(len(FILE)):
        for i in range(len(FILE)):
            files += "<sper>" + FILE[x][i] 
    return files

def session_key(receiver,Sender):


    db = sql.connect("test.db")

    sec_key = db.execute(
        "SELECT session_key from Files WHERE Sender = (?) and name = (?) ", (Sender,receiver))
    sec_key = sec_key.fetchall()
    if len(sec_key) == 0:
        return False

    db.close()
 
    return sec_key[0]
    
def get_all():
    conn = sql.connect('test.db')

    cursor = conn.execute("SELECT * from Files")
    for row in cursor:
        print("receiver = ", row[0])
        print("file path = ", row[1])
        print("Send by = ", row[2], '\n')

    conn.close()


  
  


# Create_User("admin","admin123")
# b()
# print(Get_User("admin","admin123"))
# create_Table()

# print(add_public_key("admin","aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))
# print(get_public_key("g")[0])
# get_all()

# print("ddd")
# print(add_File("admin","ewewdwedw","abdullah"))
# print(get_File("g").split('<sper>'))
# print(get_File_count("admin"))
# print(session_key("g","admin")[0])



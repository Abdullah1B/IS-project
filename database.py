import sqlite3 as sql

# def create_Table():
#     con = sql.connect("test.db")
#     cur = con.cursor()
#     qurey = '''CREATE TABLE Public_Keys
#                 ( Uname     varchar (255) not null,
#                   Public_Key char(512) NOT NULL,
#                   FOREIGN KEY(Uname) REFERENCES  USERS (Username)


#                 );
    
    
#     '''
#     con.execute(qurey)
#     con.commit()

#     con.close()
    
    
    
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
    
    

def get_all():
    conn = sql.connect('test.db')

    cursor = conn.execute("SELECT * from Public_Keys")
    for row in cursor:
        print("Username = ", row[0])
        print("Password = ", row[1], '\n')

    conn.close()


# Create_User("admin","admin123")
# b()
# print(Get_User("admin","admin123"))
# create_Table()

# print(add_public_key("admin","aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))
print(get_public_key("admin"))
# get_all()
import sqlite3 as sql
from xmlrpc.client import boolean


def Create_User(Username, Password) -> bool:
    db = sql.connect("test.db")

    sql2 = ''' INSERT INTO USERS(Username,Password)
              VALUES(?,?) '''
    try:
        db.execute(sql2, (Username, Password))
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


def b():
    conn = sql.connect('test.db')

    cursor = conn.execute("SELECT * from USERS")
    for row in cursor:
        print("Username = ", row[0])
        print("Password = ", row[1], '\n')

    conn.close()


# Create_User("admin","admin123")
# b()
# print(Get_User("admin","admin123"))

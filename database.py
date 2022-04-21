import sqlite3 as sql

def get(qurey):
    db = sql.connect('test.sqlite')
    cursorObj = db.cursor()
    
    
    
    result = cursorObj.execute(qurey)

    result = result.fetchall()
    if len(result) == 0:
        return "False"

    db.close()

    return result[0][0]

def add(qurey):
    db = sql.connect("test.sqlite")
    cursorObj = db.cursor()
    try:
        cursorObj.execute(qurey)
        db.commit()
        db.close()
        return True
    except sql.IntegrityError:
        return False

def delete(qurey):
    db = sql.connect("test.sqlite")
    cursorObj = db.cursor()
    try:
        cursorObj.execute(qurey)
        db.commit()
        db.close()
        return True
 
    except sql.DatabaseError:
        return False
    
def get_Files(Username):
    db = sql.connect("test.sqlite")

    File = db.execute(
        "SELECT path , Sender from Files WHERE name = (?) ", (Username,))
    dates = db.execute(
        "SELECT  date from Files WHERE name = (?) ", (Username,))
    File = File.fetchall()
    dates = dates.fetchall()


    db.close()
    FILE = File
    files =""
    date =""
    for i in range(len(dates)):
        date +=  dates[i][0]+"<sper>"

    for x in range(len(FILE)):
        for i in range(2):
            files += "<sper>" + FILE[x][i] 
    return files , len(FILE) , date


 

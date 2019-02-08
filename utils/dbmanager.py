import time, datetime, os, re, sys, sqlite3, json, io 

from datetime import datetime

from requests import get
import sqlite3 as lite

from datetime import date, datetime
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
cf = sqlite3.connect('inshorts.db', check_same_thread=False)

cursors = cf.cursor()
def savedb():
    db = sqlite3.connect('inshorts.db')
    db.row_factory = sqlite3.Row
    c = db.cursor()
    c.execute('SELECT * FROM files ORDER BY ID') 
    result = [dict(row) for row in c.fetchall()]
    if result is None:
        stfid  = 0 
    else: 
      with open('file.json', 'w') as outfile:  
        json.dump(result, outfile)  
      with open("file.json") as json_file:  
        data = json.load(json_file) 
      for p in data:
   
        print('ID: {}'.format(p['ID']))
        print('Name: ' + p['Fname']) 
        print('Website: ' + p['FileId'])
        print('Date: ' + p['Date'])
        print('Size: ' + p['Size']) 
        print('')
      stfid = 1 
      
      
    c.close()    
    return (stfid)  
 
  
def loadDB(): 
    # Creates SQLite database to store info.
    conn = sqlite3.connect('inshorts.db')
    cur = conn.cursor()
    conn.text_factory = str
    cur.executescript('''CREATE TABLE IF NOT EXISTS Users
    (
    id INTEGER NOT NULL PRIMARY KEY UNIQUE, 
    ChatID INTEGER, 
    LastNewsID INTEGER,
    Lang TEXT,
    UserID TEXT);'''
    )
    #cur.executescript('''DROP TABLE IF EXISTS Users;''')
    cur.executescript('''CREATE TABLE IF NOT EXISTS files
    (
    ID INTEGER NOT NULL PRIMARY KEY UNIQUE,
    Fname TEXT, 
    Size TEXT,
    FileId INTEGER,
    Date TEXT,
    Time TEXT);'''
    )
    conn.commit()
    conn.close()
       
def fetchNews(fn, fs, fid):
    conn = sqlite3.connect('inshorts.db')
    cur = conn.cursor()
    title = fn
    content = fid
    fsize = fs 
    times = datetime.now().strftime("%I:%M%p")
    dates = datetime.now().strftime("%B %d, %Y")
    
    count = 0 
    cur.execute('''SELECT Fname FROM files WHERE Fname = ? OR FileId = ?''', (title, content))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO files (Fname, FileId, Size, Date, Time) VALUES ( ?, ?, ?, ?, ? )''', (title, content, fsize, dates, times ))
        count += 1 
    conn.commit()

    print ("Total news written to database : ", count)

    cur.close()

def checkUserLastNews(chat_id):
    conn = sqlite3.connect('inshorts.db')
    cur = conn.cursor()
    cur.execute('SELECT LastNewsID FROM Users WHERE ChatID = ?', (chat_id, ))
    row = cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Users (ChatID, LastNewsID) VALUES (? , ?)', (chat_id, 1))
        LastReadNewsID = 1
        print ("\nNew User :", chat_id, "\nLast Read News ID =", LastReadNewsID)
    else:
        LastReadNewsID = row[0]
        print ("\nOld User :", chat_id, "\nLast Read News ID =", LastReadNewsID)
    conn.commit()
    cur.close()
    return LastReadNewsID 

def checkTodayFirstNewsID():
    conn = sqlite3.connect('inshorts.db')
    cur = conn.cursor()
    now = datetime.now()
    date = now.strftime("%B %d, %Y")
    likeDate = "%" + date + "%"
    cur.execute('''SELECT ID FROM files WHERE Date LIKE ? ORDER BY ID ASC LIMIT 1''', (likeDate, ))
    row = cur.fetchone()
    if row is None:
        TodayFirstNewsID = 0
        print ("\nToday First News :", "No news")
    else: 
        TodayFirstNewsID = row[0]
        print ("\nToday First News :", TodayFirstNewsID)
    cur.close()
    return TodayFirstNewsID

def fileid(fid):
    conn = sqlite3.connect('inshorts.db')
    cur = conn.cursor() 
    likeDate = "%" + fid + "%"  
    cur.execute("SELECT ID, Date, Fname, FileId, Time, Size, Time FROM files WHERE Fname LIKE ? ORDER BY ID ASC LIMIT 1", (likeDate, ))
    row = cur.fetchone()
    if row is None:
        news = "Ioh!!!!!!!."
    else: 
        
        news = row[1]
    cur.close()  
    return (news) 
def sfileid(fid):
    conn = sqlite3.connect('inshorts.db')
    cur = conn.cursor() 
    likeDate = "%" + fid + "%"  
    cur.execute("SELECT ID, Date, Fname, FileId, Time, Size, Time FROM files WHERE Fname LIKE ? ORDER BY ID ASC LIMIT 1", (likeDate, ))
    row = cur.fetchone()
    if row is None:
        tfid  = 0 
    else: 
        tfid = row[3] 
    cur.close()  
    return (tfid) 
def getNews(LastReadNewsID, chat_id):
    conn = sqlite3.connect('inshorts.db')
    cur = conn.cursor()
    print (LastReadNewsID)
    cur.execute("SELECT ID, Date, Fname, FileId, Time, Size, Time FROM files WHERE ID > ? ORDER BY ID ASC LIMIT 1", (LastReadNewsID, ))
    row = cur.fetchone()
    if row is None:
        news = "Added to my db for future use. You can see all your saved files using /myfiles."
    else:
        
        news = row[1] + "\n\n" + row[2] + "\n\n" + row[3]
        
        cursor = conn.execute("UPDATE Users SET `LastNewsID` = ? WHERE ChatID = ?", (row[0], chat_id))
    conn.commit()
    cur.close()  
    return (news)

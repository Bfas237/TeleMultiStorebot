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
def add_column_to_table(c, table_name, column_name, column_type, default, value):
    for row in c.execute('PRAGMA table_info({})'.format(table_name)):
        if row[1] == column_name:
            print('column {} already exists in {}'.format(column_name, table_name))
            break
    else:
        print('add column {} to {}'.format(column_name, table_name))
        c.execute('ALTER TABLE {} ADD COLUMN {} {} {} {}'.format(table_name, column_name, column_type, default, value))

c = cf.cursor()  
now = datetime.now()
y = int(now.strftime("%Y"))
mm = int(now.strftime("%m")) 
d = int(now.strftime("%d"))
h = int(now.strftime("%H"))
m = int(now.strftime("%M"))
s = int(now.strftime("%S")) 
#add_column_to_table(c, 'files', 'Hour', 'INTEGER', 'DEFAULT', h)   
#add_column_to_table(c, 'files', 'Minute', 'INTEGER', 'DEFAULT', m) 
#add_column_to_table(c, 'files', 'Seconds', 'INTEGER', 'DEFAULT', s) 
  
#add_column_to_table(c, 'files', 'Year', 'INTEGER', 'DEFAULT', y)   
#add_column_to_table(c, 'files', 'Month', 'INTEGER', 'DEFAULT', mm) 
#add_column_to_table(c, 'files', 'Day', 'INTEGER', 'DEFAULT', d)  
#add_column_to_table(c, 'files', 'User', 'TEXT') 
def loadDB(): 
    # Creates SQLite database to store info.
    conn = sqlite3.connect('inshorts.db', check_same_thread=False)
    cur = conn.cursor()
    conn.text_factory = str
    cur.executescript('''CREATE TABLE IF NOT EXISTS Users
    (
    id INTEGER NOT NULL PRIMARY KEY UNIQUE, 
    ChatID INTEGER, 
    LastNewsID INTEGER,
    UserID TEXT);''' 
    )
    #cur.executescript('''DROP TABLE IF EXISTS files;''') 
    
    cur.executescript('''CREATE TABLE IF NOT EXISTS Ytube
    (
    id INTEGER NOT NULL PRIMARY KEY UNIQUE, 
    ChatID INTEGER,
    Title TEXT NOT NULL,
    Thumb TEXT NOT NULL,
    FileId TEXT NOT NULL,
    Date TEXT,
    Time TEXT,
    Link TEXT
    Link_id TEXT);'''
    )
    
    cur.executescript('''CREATE TABLE IF NOT EXISTS files
    (
    ID INTEGER NOT NULL PRIMARY KEY UNIQUE,
    Fname TEXT, 
    Size TEXT,
    FileId INTEGER,
    Date TEXT,
    Time TEXT,
    DownloadId TEXT,
    Link TEXT,
    User TEXT);'''
    )  
    conn.commit()
    conn.close()
       
def fetchNews(fn, fs, fid, dlid, times, dates, user, link):
    conn = sqlite3.connect('inshorts.db', check_same_thread=False)
    cur = conn.cursor()
    title = fn
    content = fid
    fsize = fs 
    downloadid = dlid
    count = 0 
    cur.execute('''SELECT Fname FROM files WHERE Fname = ? OR FileId = ?''', (title, content))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO files (Fname, FileId, Size, Date, Time, DownloadId, User, Link) VALUES ( ?, ?, ?, ?, ?, ?, ?, ? )''', (title, content, fsize, dates, times, downloadid, user, link ))
        count += 1 
    conn.commit()

    print ("Total news written to database : ", count)

    cur.close()
def Ycheck(fn, fs, fid, dlid, times, dates, user, link):
    conn = sqlite3.connect('inshorts.db', check_same_thread=False)
    cur = conn.cursor()
    title = fn
    thumb = fid
    link = fs 
    link_id = dlid
    count = 0 
    cur.execute('''SELECT Link_id FROM Ytube WHERE Title = ? OR Link_id = ?''', (title, content))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Ytube (Title, Link_id, Thumb, Date, Time, Link, ChatID) VALUES ( ?, ?, ?, ?, ?, ?, ? )''', (title, link_id, thumb, dates, times, link, user ))
        count += 1 
    conn.commit()

    print ("Total news written to database : ", count)

    cur.close()


def checkUserLastNews(chat_id):
    conn = sqlite3.connect('inshorts.db', check_same_thread=False)
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
    conn = sqlite3.connect('inshorts.db', check_same_thread=False)
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
    conn = sqlite3.connect('inshorts.db', check_same_thread=False)
    cur = conn.cursor() 
    likeDate = "%" + fid + "%"  
    cur.execute("SELECT ID, Date, Fname, FileId, Time, Size, Time, DownloadId, User, Link FROM files WHERE DownloadId LIKE ? ORDER BY ID ASC LIMIT 1", (likeDate, ))
    row = cur.fetchone()
    if row is None:
        news = 0
    else: 
        news = row[3]
    cur.close()  
    return news

def vfileid(fid):
    conn = sqlite3.connect('inshorts.db', check_same_thread=False)
    cur = conn.cursor() 
    likeDate = "%" + fid + "%"  
    cur.execute("SELECT ID, Date, Fname, FileId, Time, Size, DownloadId, User, Link FROM files WHERE DownloadId LIKE ? ORDER BY ID ASC LIMIT 1", (likeDate, ))
    row = cur.fetchone()
    if row is None:
        news = 0
    else: 
        news = row[0], row[2], row[3], row[1], row[4], row[5], row[6]
    cur.close()  
    return news  
def ufil(fid, user):
    conn = sqlite3.connect('inshorts.db', check_same_thread=False)
    cur = conn.cursor() 
    likeDate = "%" + fid + "%"  
    cur.execute("SELECT ID, Date, Fname, FileId, Time, Size, DownloadId, User, Link, Year, Month, Day, Hour, Minute, Seconds FROM files WHERE User = ? AND DownloadId LIKE ? ORDER BY ID ASC LIMIT 1", (user, likeDate, ))
    row = cur.fetchone()
    if row is None: 
        news = 0
    else: 
        news = row[7]  
    cur.close()  
    return news   

def checkd(id, q):
    conn = sqlite3.connect('inshorts.db', check_same_thread=False)
    cur = conn.cursor()
    now = datetime.now()
    date = now.strftime("%B %d, %Y")
    likeDate = "%" + q + "%"
    TodayFirstNewsID = ""
    items = ""
    cur.execute("SELECT DownloadId from files WHERE User = ? AND DownloadId LIKE ? ORDER BY ID ASC LIMIT 1", (id, likeDate, ))
    row = cur.fetchone()
    if row is not None:
        TodayFirstNewsID = row[0]
        print ("\nUploader :", TodayFirstNewsID)
    else: 
        TodayFirstNewsID = None
        print ("\nGuest :", "Not the uploader")
        
    cur.close()
    return TodayFirstNewsID
  
  
 
def cdate(fid):
    conn = sqlite3.connect('inshorts.db', check_same_thread=False)
    cur = conn.cursor() 
    likeDate = "%" + fid + "%"  
    cur.execute("SELECT ID, Date, Fname, FileId, Time, Size, DownloadId, User, Link, Year, Month, Day, Hour, Minute, Seconds FROM files WHERE DownloadId LIKE ? ORDER BY ID ASC LIMIT 1", (likeDate, ))
    row = cur.fetchone()
    if row is None:
        news = 0
    else: 
        news = row[9], row[10], row[11], row[12], row[12], row[13]
    cur.close()  
    return news   
  
def doc(fid):
    conn = sqlite3.connect('inshorts.db', check_same_thread=False)
    cur = conn.cursor() 
    likeDate = "%" + fid + "%"  
    cur.execute("SELECT Fname, DownloadId FROM files WHERE Fname LIKE ? ORDER BY ID DESC LIMIT 1", (likeDate, )) 
    row = cur.fetchone()
    if row is None: 
        news = 0
        
    else: 
        news = row[1]
    cur.close()  
    return news  
def delid(fid): 
    conn = sqlite3.connect('inshorts.db', check_same_thread=False)
    cur = conn.cursor() 
    cur.execute("DELETE FROM files WHERE DownloadId= (?) AND User= (?)", (tnews, chat_id, ))
    row = cur.fetchone()
    if row is None:
        news = 0
    else: 
        news = row[3]
    cur.close()  
    return news

def filen(fid):
    conn = sqlite3.connect('inshorts.db', check_same_thread=False)
    cur = conn.cursor() 
    likeDate = "%" + fid + "%"  
    cur.execute("SELECT ID, Date, Fname, FileId, Time, Size, Time, DownloadId, User, Link FROM files WHERE Fname LIKE ? ORDER BY ID ASC LIMIT 1", (likeDate, ))
    row = cur.fetchone()
    if row is None:
        news = 0
    else: 
        news = row[7]    
    cur.close()  
    return news
def sfileid(fid):
    conn = sqlite3.connect('inshorts.db', check_same_thread=False)
    cur = conn.cursor() 
    likeDate = "%" + fid + "%"  
    cur.execute("SELECT ID, Date, Fname, FileId, Time, Size, Time, DownloadId, User, Link FROM files WHERE Link LIKE ? ORDER BY ID ASC LIMIT 1", (likeDate, ))
    row = cur.fetchone()
    if row is None:
        tfid  = 0 
        size = 0
    else: 
        tfid = row[3] 
        size = row[5]
    cur.close()  
    return (tfid, size) 
def getNews(LastReadNewsID, chat_id):
    conn = sqlite3.connect('inshorts.db', check_same_thread=False)
    cur = conn.cursor()
    print (LastReadNewsID)
    cur.execute("SELECT ID, Date, Fname, FileId, Size, Time, DownloadId, User, Link FROM files WHERE ID > ? ORDER BY ID ASC LIMIT 1", (LastReadNewsID, ))
    row = cur.fetchone()
    if row is None:
        news = "Saved for future use. You can see all your saved files using /files."
    elif(row[0] > LastReadNewsID):
        
        news = "Ok I got it. Access your library using /files."
    else:
        news = ""
        cursor = conn.execute("UPDATE Users SET `LastNewsID` = ? WHERE ChatID = ?", (row[0], chat_id))
    conn.commit()
    cur.close()  
    return (news)
  


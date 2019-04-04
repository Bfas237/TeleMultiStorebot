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
  
class DBHelper:
       def __init__(self, dbname="inshorts.db"):
            self.dbname = dbname
            self.conn = sqlite3.connect(dbname, check_same_thread=False)
            self.c = self.conn.cursor()
            self.setup()
    
       
       def __enter__(self):
       
            return self
      
       def setup(self):
            self.conn.text_factory = str
            self.c.executescript('''CREATE TABLE IF NOT EXISTS Users
    (
    id INTEGER NOT NULL PRIMARY KEY UNIQUE, 
    ChatID INTEGER, 
    LastNewsID INTEGER,
    UserID TEXT);''' 
    )
            #self.c.executescript('''DROP TABLE IF EXISTS files;''') 
    
            self.c.executescript('''CREATE TABLE IF NOT EXISTS files
    (
    ID INTEGER NOT NULL PRIMARY KEY UNIQUE,
    Fname TEXT, 
    Size TEXT,
    FileId INTEGER,
    Date TEXT,
    Time TEXT,
    DownloadId TEXT,
    Link TEXT,
    User TEXT,
    Private INTEGER,
    Year INTEGER,
    Month INTEGER,
    Day INTEGER,
    Hour INTEGER,
    Minute INTEGER,
    Seconds INTEGER);'''
    )  
    
            self.conn.commit()
      
       def checkifexist(self, item_text, owner):
            likeDate = "%" + str(item_text) + "%"
            self.c.execute("SELECT DownloadId, User FROM files WHERE User= (?) AND DownloadId LIKE ?", (owner, likeDate, )) 
            user = self.c.fetchone()
            if user is not None:
                return user[1]
            else: 
                return None
      
       def returnfid(self, item_text, owner):
            likeDate = "%" + str(item_text) + "%"
            self.c.execute("SELECT FileId FROM files WHERE User= (?) AND DownloadId LIKE ?", (owner, likeDate, )) 
            user = self.c.fetchone()
            if user is not None:
                return user[0]
            else: 
                return None
        
       def checkfileid(self, item_text, owner):
            likeDate = "%" + str(item_text) + "%"
            self.c.execute("SELECT FileId, User FROM files WHERE User= (?) AND FileId LIKE ?", (owner, likeDate, )) 
            user = self.c.fetchone()
            if user is not None:
                return user[0]
            else: 
                return None
        
       def fetchNews(self, fn, fs, fid, dlid, times, dates, user, link, year, month, day, h, m, s, priv):
            title = fn
            content = fid
            fsize = fs 
            downloadid = dlid
            count = 0 
            self.c.execute('''SELECT Fname FROM files WHERE Fname = ? OR FileId = ?''', (title, content))
            row = self.c.fetchone()
            if row is None:
                self.c.execute('''INSERT INTO files (Fname, FileId, Size, Date, Time, DownloadId, User, Link, Year, Month, Day, Hour, Minute, Seconds, Private) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', (title, content, fsize, dates, times, downloadid, user, link, year, month, day, h, m, s, priv ))
                count += 1 
            self.conn.commit()

            print ("Total news written to database : ", count)
        
       def checkUserLastNews(self, chat_id):
    
            self.c.execute('SELECT LastNewsID FROM Users WHERE ChatID = ?', (chat_id, ))
            row = self.c.fetchone()
            if row is None:
                self.c.execute('INSERT INTO Users (ChatID, LastNewsID) VALUES (? , ?)', (chat_id, 1))
                LastReadNewsID = 1
                print ("\nNew User :", chat_id, "\nLast Read News ID =", LastReadNewsID)
            else:
                LastReadNewsID = row[0]
                print ("\nOld User :", chat_id, "\nLast Read News ID =", LastReadNewsID)
            self.conn.commit()
    
            return LastReadNewsID 
      
       def checkTodayFirstNewsID(self):
            now = datetime.now()
            date = now.strftime("%B %d, %Y")
            likeDate = "%" + date + "%"
            self.c.execute('''SELECT ID FROM files WHERE Date LIKE ? ORDER BY ID ASC LIMIT 1''', (likeDate, ))
            row = self.c.fetchone()
            if row is None:
                TodayFirstNewsID = 0
                print ("\nToday First News :", "No news")
            else: 
                TodayFirstNewsID = row[0]
                print ("\nToday First News :", TodayFirstNewsID)
            return TodayFirstNewsID
    
    
       def fileid(self, fid):
            likeDate = "%" + fid + "%" 
            self.c.execute("SELECT ID, Date, Fname, FileId, Time, Size, Time, DownloadId, User, Link FROM files WHERE DownloadId LIKE ? ORDER BY ID ASC LIMIT 1", (likeDate, ))
    
            row = self.c.fetchone()
            if row is None:
                news = 0
            else: 
                news = row[3]
            return news
       
       def vfileid(self, fid):
            likeDate = "%" + fid + "%"
            self.c.execute("SELECT ID, Date, Fname, FileId, Time, Size, DownloadId, User, Link FROM files WHERE DownloadId LIKE ? ORDER BY ID ASC LIMIT 1", (likeDate, ))
            row = self.c.fetchone() 
            if row is None:
                news = 0
            else: 
                news = row[0], row[2], row[3], row[1], row[4], row[5], row[6]
            return news  
       
       

       def ufil(self, fid, user):
            likeDate = "%" + fid + "%" 
            self.c.execute("SELECT ID, Date, Fname, FileId, Time, Size, DownloadId, User, Link, Year, Month, Day, Hour, Minute, Seconds FROM files WHERE User = ? AND DownloadId LIKE ? ORDER BY ID ASC LIMIT 1", (user, likeDate, ))
            row = self.c.fetchone()
            if row is None: 
                news = 0
            else: 
                news = row[7]  
            return news  
          
       def checkd(self, id, q):
            now = datetime.now()
            date = now.strftime("%B %d, %Y")
            likeDate = "%" + q + "%"
            TodayFirstNewsID = ""
            items = ""
            self.c.execute("SELECT DownloadId from files WHERE User = ? AND DownloadId LIKE ? ORDER BY ID ASC LIMIT 1", (id, likeDate, ))
            row = self.c.fetchone()
            if row is not None:
                TodayFirstNewsID = row[0]
            else: 
                TodayFirstNewsID = None
            return TodayFirstNewsID
          
       def cdate(self, fid):
    
            likeDate = "%" + fid + "%"  
            self.c.execute("SELECT ID, Date, Fname, FileId, Time, Size, DownloadId, User, Link, Year, Month, Day, Hour, Minute, Seconds FROM files WHERE DownloadId LIKE ? ORDER BY ID ASC LIMIT 1", (likeDate, ))
    
            row = self.c.fetchone()
            if row is None:
                news = 0
            else: 
                news = row[9], row[10], row[11], row[12], row[12], row[13]
            return news   
  
        
          
       def doc(self, fid):
    
            likeDate = "%" + fid + "%"  
            self.c.execute("SELECT Fname, DownloadId FROM files WHERE Fname LIKE ? ORDER BY ID DESC LIMIT 1", (likeDate, )) 
            row = self.c.fetchone()
            if row is None: 
                news = 0
        
            else: 
                news = row[1]
     
            return news  
    
       
       def cdate(self, fid):
    
            likeDate = "%" + fid + "%"  
            self.c.execute("SELECT ID, Date, Fname, FileId, Time, Size, DownloadId, User, Link, Year, Month, Day, Hour, Minute, Seconds FROM files WHERE DownloadId LIKE ? ORDER BY ID ASC LIMIT 1", (likeDate, ))
    
            row = self.c.fetchone()
            if row is None:
                news = 0
            else: 
                news = row[9], row[10], row[11], row[12], row[12], row[13]
            return news   


       def delid(self, fid): 
            self.c.execute("DELETE FROM files WHERE DownloadId= (?) AND User= (?)", (tnews, chat_id, ))
            row = self.c.fetchone()
            if row is None:
                news = 0
            else: 
                news = row[3]
     
            return news
    
       def filen(self, fid):
    
            likeDate = "%" + fid + "%"  
            self.c.execute("SELECT ID, Date, Fname, FileId, Time, Size, Time, DownloadId, User, Link FROM files WHERE Fname LIKE ? ORDER BY ID ASC LIMIT 1", (likeDate, ))
            row = self.c.fetchone()
            if row is None:
                news = 0
            else: 
                news = row[7]    
     
            return news
    
       def sfileid(self, fid):
    
            likeDate = "%" + fid + "%"  
            self.c.execute("SELECT ID, Date, Fname, FileId, Time, Size, Time, DownloadId, User, Link FROM files WHERE Link LIKE ? ORDER BY ID ASC LIMIT 1", (likeDate, ))
            row = self.c.fetchone()
            if row is None:
                tfid  = 0 
                size = 0
            else: 
                tfid = row[3] 
                size = row[5]
     
            return (tfid, size) 


       def getNews(self, LastReadNewsID, chat_id):
            self.c.execute("SELECT ID, Date, Fname, FileId, Size, Time, DownloadId, User, Link FROM files WHERE ID > ? ORDER BY ID ASC LIMIT 1", (LastReadNewsID, ))
            row = self.c.fetchone()
            if row is None:
                news = "Saved for future use. You can see all your saved files using /files."
            elif(row[0] > LastReadNewsID):
        
                news = "Ok I got it. Access your library using /files."
            else:
                news = ""
                cursor = self.conn.execute("UPDATE Users SET `LastNewsID` = ? WHERE ChatID = ?", (row[0], chat_id))
            self.conn.commit()
     
            return (news)      
 
       def make_public(self, dlid, chat_id):
            likeDate = "%" + dlid + "%" 
            self.c.execute('SELECT Private, User FROM files WHERE User = ? AND DownloadId LIKE ? ORDER BY ID ASC LIMIT 1', (chat_id, dlid, ))
            row = self.c.fetchone() 
            ok = 0
            if row is not None: 
              LastReadNewsID = row[0]
                
              self.conn.execute("UPDATE OR IGNORE files SET `Private` = ? WHERE Private = 1 AND DownloadId = ?", (ok, dlid))
            else:
              LastReadNewsID = 1
            self.conn.commit()
            return LastReadNewsID  
 
       def make_private(self, dlid, chat_id):
            likeDate = "%" + dlid + "%" 
            self.c.execute('SELECT Private, User FROM files WHERE User = ? AND DownloadId LIKE ? ORDER BY ID ASC LIMIT 1', (chat_id, dlid, ))
            row = self.c.fetchone() 
            ok = 1 
            if row is not None: 
              LastReadNewsID = row[0]
                
              self.conn.execute("UPDATE OR IGNORE files SET `Private` = ? WHERE Private = 0 AND DownloadId = ?", (ok, dlid))
            else:
              LastReadNewsID = 0
            self.conn.commit()
            return LastReadNewsID 
          
       def getuser(self, fid, owner):
            likeDate = "%" + fid + "%" 
            self.c.execute('''SELECT DISTINCT User FROM files WHERE User = ? AND Private = 1 AND DownloadId LIKE ? limit 1''', (owner, likeDate, ))
            user = self.c.fetchone()
            if user is not None:   
                return user[0]
            else:
                return 0
        
       def copy(self, dlid, tnews, times, dates, chat_id, year, month, day, hr, mins, sec):
            likeDate = "%" + dlid + "%"
            self.c.execute('SELECT Fname, FileId, Size, Link, DownloadId FROM files WHERE DownloadId LIKE ? ORDER BY ID ASC LIMIT 1', (dlid, ))
            row = self.c.fetchone() 
            if row is not None: 
                self.c.execute('INSERT OR IGNORE INTO files (Fname, FileId, Size, Date, Time, DownloadId, User, Link, Year, Month, Day, Hour, Minute, Seconds) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (row[0], row[1], row[2], dates, times, tnews, chat_id, row[3], year, month, day, hr, mins, sec, ))
                LastReadNewsID = tnews
                print ("\nnNew file token :", dlid, "\nLast Read News ID =", LastReadNewsID)
            else:
                LastReadNewsID = None
                print ("\nOld  file token :", dlid, "\nLast Read News ID =", LastReadNewsID)
            self.conn.commit()
            return LastReadNewsID 

                
       def delete_item(self, item_text,owner):
                stmt="DELETE FROM files WHERE DownloadId= (?) AND User= (?)"
                args=(item_text,owner )
                self.conn.execute(stmt,args)
                self.conn.commit() 
                
                
       def delete_all(self, owner):
                stmt="DELETE FROM files WHERE User= (?)"
                args=(owner )
                self.conn.execute(stmt,args)
                self.conn.commit() 
                
       def add_column_to_table(self, table_name, column_name, column_type, default, value):
    
                for row in self.c.execute('PRAGMA table_info({})'.format(table_name)):
                    if row[1] == column_name:
                        print('column {} already exists in {}'.format(column_name, table_name))
                        return
                    else:
                        print('add column {} to {}'.format(column_name, table_name))
                        self.c.execute('ALTER TABLE {} ADD COLUMN {} {} {} {}'.format(table_name, column_name, column_type, default, value))

    
       def __exit__(self, exc_class, exc, traceback):
        
            self.conn.commit()
        
            self.conn.close()

db = DBHelper()
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
#db.add_column_to_table('files', 'Private', 'BOOL', 'DEFAULT', 0)  
  





  



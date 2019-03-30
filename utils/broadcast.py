
import sqlite3 
from datetime import datetime, timezone, date

class DBHelper:
    
    def __init__(self, dbname="teledata.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)
        self.c = self.conn.cursor()
        self.setup()
# id INTEGER AUTOINCREMENT,
    def setup(self):
        #self.c.executescript('''DROP TABLE IF EXISTS data;''')
        stmt = """CREATE TABLE IF NOT EXISTS data ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    contacted INTEGRER NULL,
                                                    tlgrm_user DEFAULT none,
                                                    key DEFAULT none                                                    
                                                   )"""
        self.c.execute(stmt)
        self.conn.commit()  

    def add_tlgrm_user(self, contacted, tlgrm_user):
        c = 0
        ok = self.c.execute("INSERT OR IGNORE INTO data (contacted, tlgrm_user) VALUES (?, ?)", (contacted, tlgrm_user))
        self.conn.commit()

    def del_tlgrm_user(self, tlgrm_id):
        likeDate = "%" + str(tlgrm_id) + "%"
        self.c.execute("DELETE FROM data WHERE tlgrm_user LIKE ?", (likeDate, ))
        self.conn.commit()  

    def checkifexist(self, tlgrm_user):
        likeDate = "%" + str(tlgrm_user) + "%"
        date = datetime.now().strftime("%B %d, %Y")
        liked = "%" + date + "%" 
        self.c.execute("SELECT DISTINCT tlgrm_user FROM data WHERE tlgrm_user = (?) AND key LIKE ?", (likeDate, liked, )) 
        
        user = self.c.fetchone()
        if user is not None:
            return user[0]
        else:
            return None

    def getusertocontact(self, limit=50):
        self.c.execute("SELECT DISTINCT tlgrm_user FROM data WHERE contacted = 0 limit "+str(limit))
        user = self.c.fetchall()
        if user is not None:
            return user
        else:
            return None

    def total(self, where = None):
        if where == 'contacted':
            self.c.execute("SELECT DISTINCT count(*) FROM data WHERE contacted IS NOT 0")
        elif where == 'notcontacted':
            self.c.execute("SELECT DISTINCT count(*) FROM data WHERE contacted = 0 ")
        else:
            self.c.execute("SELECT DISTINCT count(*) FROM data ")
        user = self.c.fetchone()
        if user is not None:
            return user[0]
        else:
            return None
    def updateuser_to_contacted(self,user):
        now = datetime.now()
        date = datetime.now().strftime("%B %d, %Y")
        likeDate = "%" + date + "%" 
        ok = 1
        self.c.execute('''UPDATE OR IGNORE data SET contacted = ?, key = ?  WHERE id = ?''', (ok, likeDate, user,))
        
        self.conn.commit()
 
    def refresh_contacted(self):
        self.c.execute('''UPDATE data SET contacted = ?''', (0,))
        self.conn.commit()
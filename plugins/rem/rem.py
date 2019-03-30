from utils.typing import *
class DBHelper:
       def __init__(self, dbname="inshorts.db"):
            self.dbname = dbname
            self.conn = sqlite3.connect(dbname, check_same_thread=False)
            self.c = self.conn.cursor()
        
       def checkifexist(self, item_text, owner):
            likeDate = "%" + str(item_text) + "%"
            self.c.execute("SELECT DownloadId, User FROM files WHERE User= (?) AND DownloadId LIKE ?", (owner, likeDate, )) 
            user = self.c.fetchone()
            if user is not None:
                return user[1]
            else: 
                return None
                
                
       def delete_item(self, item_text,owner):
                stmt="DELETE FROM files WHERE DownloadId= (?) AND User= (?)"
                args=(item_text,owner )
                self.conn.execute(stmt,args)
                self.conn.commit() 
                 
db= DBHelper()

@Client.on_message(Filters.regex("rem_"))
def my_handler(bot, m):
    chat_id = m.chat.id
    user = m.from_user.id
    h = m.text
    tnews = h[5:] 
    apk_string = "{}".format("apks")
    
    conn = sqlite3.connect('inshorts.db')
    try:
      if tnews:
        chat_id = str(user)
        report = "**❗Report:**\n\n✅ File successfully deleted from your storage:\n\nSend /files to see your download history"
        err = "\n**❌ Invalid file token:**\n\nUse /help to learn more about me"
        nauth = "\n**⚠️ 506 Unknown Error:**\n\n You are not authorised to delete this file because are not the owner\n\n Your uploaded file can be accessed using /files"
        snews = fileid(tnews)
        ver = db.checkifexist(tnews, chat_id)
        if snews: 
          if (ver == chat_id):
            db.delete_item(tnews, chat_id)
            m.reply(report)
          else:
            m.reply(nauth)
        else:
          m.reply(err)
      else:
        bot.send_chat_action(chat_id,'TYPING')
        time.sleep(1.5)
        m.reply("Syntax error. Press /help for more info")
 
    except Exception as e:
        m.reply(str(e))

       
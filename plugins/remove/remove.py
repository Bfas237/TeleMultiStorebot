from utils.typing import *
class DBHelper:
       def __init__(self,dbname="inshorts.db"):
                self.dbname=dbname
                self.conn=sqlite3.connect(dbname)
                
                
       def delete_item(self, item_text,owner):
                stmt="DELETE FROM files WHERE DownloadId= (?) AND User= (?)"
                args=(item_text,owner )
                self.conn.execute(stmt,args)
                self.conn.commit() 
                
db= DBHelper()
    
@Client.on_message(Filters.regex("remove_"))
def my_handler(bot, m):
    chat_id = m.chat.id
    user = m.from_user.id
    h = m.text
    tnews = h[8:] 
    apk_string = "{}".format("apks")
    
    conn = sqlite3.connect('inshorts.db')
    try:
      if tnews:
        chat_id = str(m.from_user.id)
        stmt="DELETE FROM files WHERE DownloadId= (?) AND User= (?)"
        args=(tnews, chat_id )
        report = "✅ File successfully deleted from your storage:\n\nSend /files to see your download history"
        err = "\n❌ Invalid file token:\n\nUse /help to learn more about me"
        snews = fileid(tnews) 
        if snews:
          conn.execute(stmt,args)
          conn.commit()
          m.reply(report)
        else:
          m.reply(err)
      else:
        bot.send_chat_action(chat_id,'TYPING')
        time.sleep(1.5)
        m.reply("Syntax error. Press /help for more info")
 
    except Exception as e:
        m.reply(str(e))

       
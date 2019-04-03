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
                

state = {}

 
      
@Client.on_message(Filters.regex("de_"))
def my_handler(bot, m):
    chat_id = m.chat.id
    user = m.from_user.id  
    ids = []
     
    ids.append(user)
    h = m.text
    if "/start" in h:
      g = h[10:]
    else:
      g = h[4:]
    admin = False 
    try:
      snews = db.fileid(g)
      if snews:
        num, row, fid, dat, tim, siz, did = db.vfileid(g)
        nums = db.checkd(str(user), g) 
      else:
        row = None 
      if row:
            user = db.ufil(did, str(user))
          
            ids.append(user) 
            
            yr, mm, day, hr, mte, sec = db.cdate(did)
            ds = datetime(yr, mm, day, hr, mte, sec )
             
            if(user != 0):
                item = (
              "🆔 :             #{} \n\n" 
              "ℹ️ :                       <b>{}</b>\n\n" 
              "⌛️ :        <i>{}</i>          |             🕰  <i>{}</i>\n\n"
              "⚖️ :                                 <i>{}</i>\n"
              "-----------------------------------------------------------------------------------------------------""".format(str(nums), str(row[:50]), dat, timedate(ds), pretty_size(int(siz)))) 
                        
                bot.send_chat_action(chat_id,'TYPING')
                time.sleep(1)
                admin = True 
            else:
                item = (
              "🆔 :             #{} \n\n" 
              "ℹ️ :                       <b>{}</b>\n\n" 
              "⌛️ :         <i>{}</i>          |              🕰  <i>{}</i>\n\n"
              "⚖️ :                                 <i>{}</i>\n"
              "-----------------------------------------------------------------------------------------------------""".format(str(nums), str(row), dat, timedate(ds), pretty_size(int(siz)))) 
                
                bot.send_chat_action(chat_id,'TYPING')
                time.sleep(1) 
                admin = False
                
            kb = reg_keyboard(id=did, admin=admin, confirmed=user in ids if user else False, ids=user, chat_id=chat_id)  
            reply_markup = InlineKeyboardMarkup(kb) 
               
            m.reply("{}\n\nPowered with ❤️ - @Bfas237Bots".format(item), parse_mode="html", reply_markup=reply_markup) 
        # + b"%" + str(dat).encode('UTF-8') + b"%" + str(tim).encode('UTF-8') + b"%" + str(siz).encode('UTF-8') + b"%" + str(did.encode('UTF-8')
      else:  
     
        bot.send_chat_action(chat_id,'TYPING')
        time.sleep(1.5)
        m.reply("😔 `404` **Invalid FILE_ID**.\n\n Send /files to see your saved files")
 
    except:
        traceback.print_exc() 
from utils.strings import * 
 
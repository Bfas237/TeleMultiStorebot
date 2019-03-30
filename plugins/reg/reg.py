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
state = {}

      
 
      
@Client.on_message(Filters.regex("de_"))
def my_handler(bot, m):
    chat_id = m.chat.id
    user = m.from_user.id
    h = m.text
    if "/start" in h:
      g = h[10:]
    else:
      g = h[4:]
    num, row, fid, dat, tim, siz, did = vfileid(g) 
    #m.reply(tnews)
    usr = ufil(g)
    #us = Client.resolve_peer("self", peer_id="Bfaschat")
    #print(us)
    apk_string = "{}".format("apks")
    try:
      if row:
        item = (
              "🆔 :  #{} \n\n" 
              "ℹ️ :  <b>{}</b>\n\n" 
              "🔄 :  /dl_{}    |    ❌  /rem_{}\n\n"
              "⌛️ :  <i>{}</i>    |    🕰  <i>{}</i>\n\n"
              "⚖️ <i>{}</i>\n"
              "------------------------------" 
              "".format(str(num), str(row[:50]), did, did, dat, tim, pretty_size(int(siz))))
        
        bot.send_chat_action(chat_id,'TYPING')
        kb = [[
        InlineKeyboardButton(
            text='⬅️ Newer',
            callback_data=b'old'
        ),
        InlineKeyboardButton(
            text='Older ➡️',
            callback_data=b'old'
        )]]
        reply_markup = InlineKeyboardMarkup(kb)
        time.sleep(1)
        m.reply("{}\n\nPowered with ❤️ - @Bfas2327Bots".format(item),
                            reply_markup=reply_markup, parse_mode="html") 
      else:  
     
        bot.send_chat_action(chat_id,'TYPING')
        time.sleep(1.5)
        m.reply("😔 `404` **Invalid FILE_ID**.\n\n Send /files to see your saved files")
 
    except Exception as e:
        m.reply(str(e))
      
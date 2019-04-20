from utils.typing import *
from utils.menus import *
                

state = {}
@Client.on_message(Filters.command("files")) 
def sendServerStartedMessage(bot, m):
    global state
    link = " ".join(m.command[1:])
    logger.info(m.text)     
    msg = m.text
    if '/files@' in link:
      logger.info(msg)  
      m.reply(msg) 
    chat_id = m.chat.id
    bot.send_chat_action(chat_id,'TYPING')
    # Connecting to the SQL database
    conn = sqlite3.connect('inshorts.db')
    c = conn.cursor()
    con = conn.cursor()
    dd = m.from_user.id
    
    try: 
      t = int(re.search(r'\d+', link).group())
      off = int(t) 
    except:
      off = 0 
    if m.from_user.id not in state: 
        state[m.from_user.id] = {'actions': []}
    state[m.from_user.id]['actions'].append('files')
    logger.warning(state) 
    chat_id = str(dd)
    c.execute("SELECT ID, Fname, DownloadId, Size FROM files WHERE User = ? ORDER BY ID DESC LIMIT 5 OFFSET ?", (chat_id, off, ))
    con.execute("SELECT COUNT (*) FROM files WHERE User = ?", (chat_id, ))
    last = 0
    rowcount = con.fetchone()[0]
    rows = c.fetchall() 
    conn.close() 
    try:  
      if len(rows) > 0: 
        items = ""
        lens = len(rows) * 0 
        for row in rows:
            items +=  (
              "<code>#{}</code> " 
              " <b>{}</b>"     
              "\n<a href='https://telegram.me/jhbjh14514jjhbot?start=dl_{}'>📥 Download</a>  | <a href='https://telegram.me/jhbjh14514jjhbot?start=de_{}'>📍 Details</a>\n"       
              "<i>{}</i>\n"  
              "------\n" 
              "".format(str(row[0]), row[1][:50], row[2], row[2], pretty_size(int(row[3]))))
        
        kb = search_keyboard(offset=0, rows=rowcount, last=last, show_download=True)
        reply_markup = InlineKeyboardMarkup(kb)
        username = m.from_user.username
        src = m.reply("📄 <b>{}</b>'s files Library:   <b>{} out of {}</b> \n\n {}".format(username, lens, rowcount, items),reply_markup = reply_markup, parse_mode="html")
        user_chat = state.get(m.from_user.id, None)
        user_chat['msg'] = None
        user_chat['msgid'] = src
        user_chat['off'] = off
      
      else:
        m.reply("No items in your list")
    except:
        traceback.print_exc()  
    

       
@Client.on_message(Filters.regex("files@")) 
def my_handler(bot, m):
    global state
    chat_id = m.chat.id
    user = m.from_user.id
    h = m.text
    if "/start" in h:
      g = h[10:]
    else:
      g = h[:6]
    #m.reply(tnews)
    #us = Client.resolve_peer("self", peer_id="Bfaschat")
    #print(us)
    bot.send_chat_action(chat_id,'TYPING')
    # Connecting to the SQL database
    conn = sqlite3.connect('inshorts.db')
    c = conn.cursor()
    con = conn.cursor()
    dd = m.from_user.id
    off = 0 
    if m.from_user.id not in state: 
        state[m.from_user.id] = {'actions': []}
    state[m.from_user.id]['actions'].append('files')
    logger.warning(state) 
    chat_id = str(user)
    c.execute("SELECT ID, Fname, DownloadId, Size FROM files WHERE User = ? ORDER BY ID DESC LIMIT 5 OFFSET ?", (chat_id, off, ))
    con.execute("SELECT COUNT (*) FROM files WHERE User = ?", (chat_id, ))
    last = 0
    rowcount = con.fetchone()[0]
    rows = c.fetchall() 
    conn.close() 
    try:  
      if len(rows) > 0: 
        items = ""
        lens = len(rows)
        for row in rows:
            items +=  (
              "<code>#{}</code> " 
              " <b>{}</b>"     
              "\n<a href='https://telegram.me/TeleMultiStoreBot?start=dl_{}'>📥 Download</a>  | <a href='https://telegram.me/TeleMultiStoreBot?start=de_{}'>📍 Details</a>\n"       
              "<i>{}</i>\n"  
              "------\n" 
              "".format(str(row[0]), row[1][:50], row[2], row[2], pretty_size(int(row[3]))))
        
        kb = search_keyboard(offset=0, rows=rowcount, last=last, show_download=True)
        reply_markup = InlineKeyboardMarkup(kb)
        username = m.from_user.username
        src = m.reply("📄 <b>{}</b>'s files Library:   <b>{} out of {}</b> \n\n {}".format(username, lens, rowcount, items),reply_markup = reply_markup, parse_mode="html")
        user_chat = state.get(m.from_user.id, None)
        user_chat['msg'] = None 
        user_chat['msgid'] = src
        user_chat['off'] = off
      
      else:
        m.reply("No items in your list")
    except:
        traceback.print_exc()
    apk_string = "{}".format("apks")
      

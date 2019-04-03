from utils.typing import *

                 
db= DBHelper()
  

            
 
 
@Client.on_callback_query()
def pyrogram_data(m, query):
    global state  
    off = 0
    update = query 
    cb = query.data
    chat_id = query.from_user.id
    data = query.data
    dataid = query.id
    
    data = data.split(b'%')
    
     
    conn = sqlite3.connect('inshorts.db') 
    c = conn.cursor()
    con = conn.cursor()
    cf = conn.cursor()
    chat_id = str(chat_id)
    action = ''
    offset = 0
    q = ''
    adm = ''
    inv = "😔 `404` **Invalid FILE_ID**.\n\n Send /files to see your saved files"
    hide = False
    disabled_attachments = set()
    confirmed = False
    show_download = False
    for elem in data:
        name, *args = elem.split(b'=')

        if name == b'act':
            action = args[0]
        if name == b'end':
            end = args[0]
        elif name == b'off':
            offset = int(args[0])
        elif name == b'noatt':
            disabled_attachments = set(int(arg) for arg in args if arg != '')
        elif name == b'adm':
            adm = int(args[0])
        elif name == b'cnf':
            confirmed = bool(int(args[0]))
        elif name == b'qry':
            q = b'='.join(args)
        elif name == b'hide':
            hide = int(args[0])
    con.execute("SELECT DISTINCT COUNT (*) FROM files WHERE User = ?", (chat_id, ))  
    
    rowcount = con.fetchone()[0]
    
    last = 0
    if action == b'old':
        new_offset = offset + 4
    elif action == b'new':
        new_offset = offset - 4
    elif action == b'first':
        new_offset = 0
      
    elif action == b'last':
      last = last + offset + 20 
      if not last > rowcount:
        new_offset = last
        show_next = False
      else:
        new_offset = rowcount - 1
        show_next = False
    else:
        new_offset = offset 
        
    logger.warning(new_offset) 
    c.execute("SELECT DISTINCT ID, Fname, DownloadId, Size FROM files WHERE User = ? ORDER BY ID DESC LIMIT 5 OFFSET ?", (chat_id, new_offset, ))
    
    rows = c.fetchall() 
    conn.close() 
    items = ""
    try:
        if len(rows) > 0: 
          lens = len(rows)
          for row in rows:
              items +=  (
              "<code>#{}</code> " 
              " <b>{}</b>"     
              "\n<a href='https://telegram.me/jhbjh14514jjhbot?start=dl_{}'>📥 Download</a>  | <a href='https://telegram.me/jhbjh14514jjhbot?start=de_{}'>📍 Details</a>\n"       
              "<i>{}</i>\n"  
              "------\n" 
              "".format(str(row[0]), row[1][:50], row[2], row[2], pretty_size(int(row[3]))))

    except (TypeError, ValueError, AttributeError):
        items = None 
      
    else:
        offset = new_offset

    reply = None
    if action in (b'old', b'new', b'last', b'first'):
        if items:
            reply = items
        elif (offset < 0):
            m.answer_callback_query(query.id, "WTF! {}, 🙄 I can't go back to the future 😏".format(query.from_user.first_name), show_alert=True)
            offset = offset + 4
            return
        elif (offset > rowcount):
            m.answer_callback_query(query.id, "Hold on! {}, That was it i have nothing more to show you 🚶🏼‍♂️🚶🏼‍♂️🚶🏼‍♂️".format(query.from_user.first_name), show_alert=True)
            offset = offset - 4
            return
        try:
          ids = [chat_id, str(hide.decode('UTF-8'))]
          confirmed = chat_id in ids if chat_id else False
        except:
          pass
    elif action == b'copy': 
        
        if not confirmed:
          report = "**❗Report:**\n\n✅ File successfully deleted from your storage:\n\nSend /files to see your download history"
          err = "\n**❌ Invalid file token:**\n\nUse /help to learn more about me"
          nauth = "\n**⚠️ 506 Unknown Error:**\n\n You are not authorised to delete this file because are not the owner\n\n Your uploaded file can be accessed using /files"
          user = db.ufil(str(q), str(chat_id))
          ids = [chat_id, str(user)]
        
          kbs =  regs_keyboard(id=str(q), admin=True, confirmed=user in ids if user else False, ids=user, chat_id=chat_id)  
          reply_markups = InlineKeyboardMarkup(kbs)
          
          link = "https://t.me/jhbjh14514jjhbot"
          download_id = generate_uuid()
          times = datetime.now().strftime("%I:%M%p")
          dates = datetime.now().strftime("%B %d, %Y")
          now = datetime.now()
          year = int(now.strftime("%Y"))
          month = int(now.strftime("%m"))
          day = int(now.strftime("%d"))
          hr = int(now.strftime("%H"))
          mins = int(now.strftime("%M"))
          sec = int(now.strftime("%S"))
          try:
              tnews = str(q.decode('UTF-8'))
              snews = db.fileid(tnews)
              #(dlid, times, dates, user, year, month, day, h, m, s)
              fids = db.copy(tnews, str(download_id+"b"), times, dates, chat_id, year, month, day, hr, mins, sec)
              if fids is not None:
                fidse = fids
              else:
                m.answer_callback_query(query.id, "There was an error")
                return
              logger.warning(fids)
              ver = db.checkifexist(fidse, chat_id)
              item = ""
              reply_markups = InlineKeyboardMarkup(kbs)
              if snews:
                num, row, fid, dat, tim, siz, did = db.vfileid(fidse)
                nums = db.checkd(chat_id, did)
              else:
                did = None
               
              if ver:
                if did:
                  yr, mm, day, hr, mte, sec = db.cdate(did)
                  ds = datetime(yr, mm, day, hr, mte, sec )
                  user = db.ufil(did, str(chat_id))
                  ids = [chat_id, str(user)]
                  kbs =  reg_keyboard(id=did, admin=True, confirmed=user in ids if user else False, ids=user, chat_id=chat_id)  
                  reply_markups = InlineKeyboardMarkup(kbs) 
                  
                  logger.warning(user)
                  
                  if(user != 0):
                      item = (
              "🆔 :             #{} \n\n" 
              "ℹ️ :                       <b>{}</b>\n\n"
              "⌛️ :         <i>{}</i>          |              🕰  <i>{}</i>\n\n"
              "⚖️ :                                 <i>{}</i>\n"
              "-----------------------------------------------------------------------------------------""".format(str(nums), str(row), dat, timedate(ds), pretty_size(int(siz))))
                    
                      
                      m.edit_message_text(chat_id=update.message.chat.id, message_id=update.message.message_id, text="{}".format(item), disable_web_page_preview=True, parse_mode="html", reply_markup=reply_markups) 
                      m.answer_callback_query(query.id, "File was removed successfully")
                      
                  else:
                    
                    m.edit_message_text(chat_id=update.message.chat.id, message_id=update.message.message_id, text="{}".format(report), disable_web_page_preview=True, reply_markup=reply_markups) 
                    m.answer_callback_query(query.id, "File was removed successfully")
                   
                else:
                  m.edit_message_text(
            chat_id=update.message.chat.id, message_id=update.message.message_id, text="{}".format(nauth), disable_web_page_preview=True, reply_markup=reply_markups) 
                  m.answer_callback_query(query.id, "You can't delete this. Why not save it first", show_alert=True) 
              else:
                m.edit_message_text(
            chat_id=update.message.chat.id, message_id=update.message.message_id, text="{}".format(err), disable_web_page_preview=True, reply_markup=reply_markups) 
                m.answer_callback_query(query.id, "The token is invalid", show_alert=True)
          except AttributeError:
              m.answer_callback_query(query.id, "The action can't be performed kindly try again", show_alert=True)
              return
        else:
          report = "**❗Report:**\n\n✅ File successfully deleted from your storage:\n\nSend /files to see your download history"
          err = "\n**❌ Invalid file token:**\n\nUse /help to learn more about me"
          nauth = "\n**⚠️ 506 Unknown Error:**\n\n You are not authorised to delete this file because are not the owner\n\n Your uploaded file can be accessed using /files"
          try:
              tnews = str(q.decode('UTF-8'))
              snews = db.fileid(tnews)
              ver = db.checkifexist(tnews, chat_id)
              ids = [chat_id, str(ver)]
              user = db.ufil(tnews, str(chat_id))
              kbs = regs_keyboard(id=tnews, admin=False, confirmed=user in ids if user else False, ids=user, chat_id=chat_id)
              reply_markups = InlineKeyboardMarkup(kbs)
              if snews: 
                if (ver == chat_id):
                  db.delete_item(tnews, chat_id)
                  m.edit_message_text(chat_id=update.message.chat.id, message_id=update.message.message_id, text="{}".format(report), disable_web_page_preview=True, reply_markup=reply_markups) 
                  m.answer_callback_query(query.id, "File was removed successfully")
                  #g = str(q.decode('UTF-8')) 
                elif not ver: 
                  m.edit_message_text(
            chat_id=update.message.chat.id, message_id=update.message.message_id, text="{}".format(nauth), disable_web_page_preview=True, reply_markup=reply_markups) 
                  m.answer_callback_query(query.id, "You can't delete this. Why not save it first", show_alert=True) 
                
                
              else:
                m.edit_message_text(
            chat_id=update.message.chat.id, message_id=update.message.message_id, text="{}".format(err), disable_web_page_preview=True, reply_markup=reply_markups) 
                m.answer_callback_query(query.id, "The token is invalid", show_alert=True)
          except (TypeError, ValueError, AttributeError):
               m.answer_callback_query(query.id, "The action can't be performed kindly try again", show_alert=True)
          except: 
              traceback.print_exc() 
        
        show_download = not confirmed
        return


    elif action == b'dl':
        user = ufil(str(q.decode('UTF-8')), str(chat_id))
        ids = [chat_id, str(user)]
        
        kbs =  regs_keyboard(id=str(q.decode('UTF-8')), admin=True, confirmed=user in ids if user else False, ids=user, chat_id=chat_id)  
        reply_markups = InlineKeyboardMarkup(kbs)
        try:
            g = str(q.decode('UTF-8'))
            snews = fileid(g)
            if snews:
                num, row, fid, dat, tim, siz, did = vfileid(g)
                nums = checkd(str(user), g) 
            else:
                fid = None 
            if fid:
                m.send_chat_action(update.message.chat.id,'UPLOAD_DOCUMENT')
                time.sleep(1)
                m.edit_message_reply_markup(update.message.chat.id, 
             update.message.message_id,reply_markups)
                time.sleep(1)
                m.send_cached_media(update.message.chat.id, fid, caption="Powered with ❤️ - @Bfas237Bots")
                
                return
            else: 
                m.send_chat_action(update.message.chat.id,'TYPING')
                time.sleep(1.5)
                inv = "😔 `404` **Invalid FILE_ID**.\n\n Send /files to see your saved files"
                m.edit_message_text(
            chat_id=update.message.chat.id, message_id=update.message.message_id, text="{}".format(inv), disable_web_page_preview=True, reply_markup=reply_markups) 
                m.answer_callback_query(query.id, "The file ID is invalid", show_alert=True)
                return
        except FileIdInvalid:
                m.answer_callback_query(query.id, "The was a problem sending this file. Thats all i know", show_alert=True)
                return 
    
    #mm =  state.get(update.message.chat.id).get('msgid')
    kb = search_keyboard(offset=offset, rows=rowcount, last=last, show_download=show_download)
    username = query.from_user.first_name
    reply_markup = InlineKeyboardMarkup(kb)
    
    if reply:
        try:
           m.edit_message_text(
            chat_id=update.message.chat.id, 
             message_id=update.message.message_id,
            text="📄 <b>{}</b>'s files Library:   <b>{} out of {}</b> \n\n {}".format(username, offset, rowcount, reply),
             parse_mode=pyrogram.ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        ) 
         
        except AttributeError as e:
          logger.debug(e)
          m.answer_callback_query(query.id, "Hold on! {}, Your session has expired 🙄:(".format(query.from_user.first_name), show_alert=True)
    else:
        m.edit_message_reply_markup(update.message.chat.id, 
             update.message.message_id,reply_markup) 
        
        
          
  
        
def reg_keyboard(id, admin, confirmed, ids, chat_id):  
    data = list()
    data.append('cnf=' + str(int(confirmed)))
    data.append('hide=' + str(int(ids)))
    data.append('qry=' + str(id))
    data.append('adm=' + str(ids))
    data = '%'.join(data)
    logger.warning(data)
    
    kb = [[
        InlineKeyboardButton( text=('💾' + ' Save this file') if not confirmed else ('🗑' + ' Remove from Storage'), callback_data=b'act=copy%' + data.encode('UTF-8') ),
        
        InlineKeyboardButton(
                text=('🗳' + ' View all Saved Files') if not confirmed else ('📦' + ' Access Your File Storage'), callback_data=b'act=first%' + data.encode('UTF-8'))
    ],
      [InlineKeyboardButton(
                text='📥 Download',
                callback_data=b'act=dl%' + data.encode('UTF-8')
            )], list()]
    
     
    return kb 

def search_keyboard(offset, rows, last, show_download):  
    data = list()
    
    data.append('off=' + str(int(offset)))
    data.append('next=' + str(int(rows)))
    data.append('dl=' + str(int(show_download)))
    data = '%'.join(data)
    last = last + offset + 20 
    if not last > rows:
        new_offset = last
        show_next = False
    else:
        new_offset = rows - 1
    if offset == 0 and not rows < offset:
      kb = [[
            InlineKeyboardButton(
                text='⬇️' + ' Goto Last Page',
                callback_data=b'act=last%' + data.encode('UTF-8')),
        
        InlineKeyboardButton(
            text='Older ➡️',
            callback_data=b'act=old%' + data.encode('UTF-8')
        ),
    ], list()]
    elif (offset == new_offset):
      kb = [[
        InlineKeyboardButton(
            text='⬅️ Newer',
            callback_data=b'act=new%' + data.encode('UTF-8')
        ),
            InlineKeyboardButton(
                text='⬆️' + ' Goto First Page',
                callback_data=b'act=first%' + data.encode('UTF-8')
            )
    ], list()] 
      
    
    elif offset > 0 and not rows < 0:
      kb = [[
        InlineKeyboardButton(
            text='⬅️ Newer',
            callback_data=b'act=new%' + data.encode('UTF-8')
        ),
        InlineKeyboardButton(
            text='Older ➡️',
            callback_data=b'act=old%' + data.encode('UTF-8')
        ),
    ], list()]
    return kb
  
  
    

 
def dl_keyboard(id, admin, confirmed, ids, chat_id):  
    data = list()
    data.append('cnf=' + str(int(confirmed)))
    data.append('hide=' + str(int(ids)))
    data.append('qry=' + str(id))
    data = '%'.join(data)
    logger.warning(data)
    kb = [[
            InlineKeyboardButton(
                text=('💾' + ' Save this file') if not confirmed else ('🗑' + ' Remove from Storage'),
                callback_data=b'act=copy%' + data.encode('UTF-8')
            )
        ], [
            InlineKeyboardButton(
                text=('🗳' + ' View all Saved Files') if not confirmed else ('📦' + ' Access Your File Storage'),
                callback_data=b'act=first%' + data.encode('UTF-8')
            )
        ]]
    return kb        
  
  
  
  
  
def regs_keyboard(id, admin, confirmed, ids, chat_id):  
    data = list()
    data.append('cnf=' + str(int(confirmed)))
    data.append('hide=' + str(int(ids)))
    data.append('qry=' + str(id))
    data = '%'.join(data)
    logger.warning(data)
    kb = [[
            InlineKeyboardButton(
                text=('🗳' + ' View all Saved Files') if not confirmed else ('📦' + ' Access Your Storage'),
                callback_data=b'act=first%' + data.encode('UTF-8')
            )
        ]]
    return kb
  

def copy_keyboard(id, admin, confirmed, ids, chat_id):  
    data = list()
    data.append('cnf=' + str(int(confirmed)))
    data.append('hide=' + str(int(ids)))
    data.append('qry=' + str(id))
    data = '%'.join(data)
    logger.warning(data)
    kb = [[
        InlineKeyboardButton( text=('💾' + ' Save this file') if not confirmed else ('🗑' + ' Remove from Storage'), callback_data=b'act=copy%' + data.encode('UTF-8') ),
        
        InlineKeyboardButton(
                text=('🗳' + ' View all Saved Files') if not confirmed else ('📦' + ' Access Your File Storage'), callback_data=b'act=first%' + data.encode('UTF-8'))
    ],
      [InlineKeyboardButton(
                text='📥 Download',
                callback_data=b'act=dl%' + data.encode('UTF-8')
            )], list()]
    return kb
  
  

    
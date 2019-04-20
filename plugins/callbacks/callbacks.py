from utils.typing import *
from utils.menus import *    
from pyrogram import (
    api, Emoji, Client, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaDocument 
)
from base64 import b64decode
from struct import unpack

def parse_inline_message_id(inline_message_id):
    inline_message_id += "=" * ((4 - len(inline_message_id) % 4) % 4) 
    dc_id, _id, access_hash = unpack("<iqq",b64decode(inline_message_id,"-_"))
    return api.types.InputBotInlineMessageID(dc_id=dc_id,id=_id,access_hash=access_hash)

@Client.on_callback_query()
def pyrogram_data(m, query):
    global state  
    off = 0
    update = query 
    cb = query.data
    uploader = query.from_user.id
    chat_id = query.message.chat.id
    logger.warning('%s and %s just pressed the keyboard button', uploader, chat_id)
    data = query.data
    dataid = query.id
    data = data.split(b'%')
    logger.warning(data)
    
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
    auth = set()
    confirmed = False
    private = 0
    show_download = False 
    admin = False
    for elem in data:
        name, *args = elem.split(b'=') 

        if name == b'act':
            action = args[0]
        elif name == b'end':
            end = args[0]
        elif name == 'query':
            link = b'='.join(args)
        elif name == b'off':
            offset = int(args[0])
        elif name == b'auth':
            auth = set(int(arg) for arg in args if arg != b'')
        elif name == b'adm':
            adm = int(args[0])
        elif name == b'cnf':
            confirmed = bool(int(args[0]))
        elif name == b'prv':
            private = bool(int(args[0]))
        elif name == b'dl':
            show_download = bool(int(args[0]))
        elif name == b'owner':
            admin = bool(int(args[0]))
        elif name == b'qry':
            q = b'='.join(args)
        elif name == b'hide':
            hide = int(args[0])
    con.execute("SELECT DISTINCT COUNT (*) FROM files")  
    
    rowcount = con.fetchone()[0]
    
    last = 0
    logger.info(q)
    if action == b'old':
        new_offset = offset + 5
    elif action == b'new':
        new_offset = offset - 5
    elif action == b'first':
        new_offset = 0
      
    elif action == b'last':
      last = last + offset + 5 
      if not last > rowcount:
        new_offset = rowcount - 1
      else:
        new_offset = rowcount - 1
        show_next = False
    else:
        new_offset = offset 
        
    logger.warning(new_offset) 
    likeDate = "%" + str(q.decode('UTF-8')) + "%"
    c.execute("SELECT ID, Fname, DownloadId, Size, Media FROM files WHERE Fname LIKE ? OR DownloadId LIKE ? OR Media LIKE ? ORDER BY ID DESC LIMIT 100 OFFSET ?", (likeDate, likeDate, likeDate, new_offset, ))
    med = ""
    su = []
    if "Software" in su:
      med = "🗳"
    elif "Music" in su:
      med = "📮"
    elif "Video" in su:
      med = "💽"
    elif "Documents" in su:
      med = "📑"
    elif "Archives" in su:
      med = "🗃"
    elif "Apps" in su:
      med = "🗂"
    elif "Pictures" in su:
      med = "🖼"
    else:
      med = "📦"
    items = ""
    rows = c.fetchall() 
    things = [list(i) for i in rows]
    for ft in things[0:49]:
      su.append(str(ft[4])) 
    try:  
        if things:
          lens = len(rows) 
          for num, row in enumerate(things[0:5]):
              items +=  (
              "<code>#{}</code> " 
              " <b>{}</b>"     
              "\n\n<a href='https://telegram.me/TeleMultiStoreBot?start=dl_{}'>📥 Download</a>  | <a href='https://telegram.me/TeleMultiStoreBot?start=de_{}'>📍 Details</a>  | ⚖️ <code>{}</code> |  {} <b>{}</b>\n"       
              "\n"  
              "-------------------------\n" 
              "\n".format(str(num), (row[1][:70] + '..') if len(row[1]) > 75 else row[1], row[2], row[2], pretty_size(int(row[3])), med, row[4]))

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
            offset = 0
        elif (offset > rowcount):
            m.answer_callback_query(query.id, "Hold on! {}, That was it i have nothing more to show you 🚶🏼‍♂️🚶🏼‍♂️🚶🏼‍♂️".format(query.from_user.first_name), show_alert=True)
            offset = offset - 5
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
          unc = "\n**⚠️ 309 Uncaught Error:**\n\nThe file you are trying to save was deleted by the original uploader. You need to resend the file to save it again"
          savetwice = "\n**⚠️ 603 NotProcessed Error:**\n\nWhy would you want to save the same file more than once? 🙄 If you wish to continue, feel free its your choice"
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
              df = db.returnfid(tnews, chat_id)
              if df is not None:
                chkfid = db.checkfileid(df, chat_id)
                if chkfid is not None:
                  m.edit_message_text(chat_id=update.message.chat.id, message_id=update.message.message_id, text="{}".format(savetwice), disable_web_page_preview=True, parse_mode="markdown", reply_markup=reply_markups) 
                  m.answer_callback_query(query.id, "The file you are trying to save is not available")
                  return
                else:
                  pass
              else:
                pass
              #(dlid, times, dates, user, year, month, day, h, m, s)
              fids = db.copy(tnews, str(download_id+"b"), times, dates, chat_id, year, month, day, hr, mins, sec)
              if fids is not None:
                fidse = fids
              else:
                m.edit_message_text(chat_id=update.message.chat.id, message_id=update.message.message_id, text="{}".format(unc), disable_web_page_preview=True, parse_mode="markdown", reply_markup=reply_markups) 
                m.answer_callback_query(query.id, "The file you are trying to save is not available")
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
                  kbs =  reg_keyboard(id=did, admin=True, confirmed=user in ids if user else False, ids=user, chat_id=chat_id, private=1, auth=[])  
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
                      m.answer_callback_query(query.id, "Wao! You just saved this to your storage. Have fun 😊")
                      
                  else:
                    
                    m.edit_message_text(chat_id=update.message.chat.id, message_id=update.message.message_id, text="{}".format(report), disable_web_page_preview=True, reply_markup=reply_markups) 
                    m.answer_callback_query(query.id, "You appear to be an alien. Why not check yur storage first", show_alert=True)
                   
                else:
                  m.edit_message_text(
            chat_id=update.message.chat.id, message_id=update.message.message_id, text="{}".format(nauth), disable_web_page_preview=True, reply_markup=reply_markups) 
                  m.answer_callback_query(query.id, "The file ID is invalid. Kindly refresh your files list", show_alert=True) 
              else:
                m.edit_message_text(
            chat_id=update.message.chat.id, message_id=update.message.message_id, text="{}".format(err), disable_web_page_preview=True, reply_markup=reply_markups) 
                m.answer_callback_query(query.id, "🙄​ Just stop the madness. The required file is missen / deleted / or may be private", show_alert=True)
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
          except TypeError as e:
              logger.debug(e)
              m.answer_callback_query(query.id, "The action can't be performed kindly try again", show_alert=True)
          except ValueError as e: 
              logger.debug(e)
              m.answer_callback_query(query.id, "308 Unidentified error... My master has been notified", show_alert=True)
              return
          except AttributeError as e: 
              logger.debug(e)
              m.answer_callback_query(query.id, "307 System error... My master has been notified", show_alert=True)
              return
        
        show_download = not confirmed
        return


    elif action == b'auth': 
        if not admin:
            did = str(q.decode('UTF-8'))
            user = db.ufil(str(q.decode('UTF-8')), str(chat_id))
            ids = [chat_id, str(user)]
            pr = db.make_private(did, str(chat_id))
            usr = db.getuser(did, str(chat_id))
            if (usr != chat_id):
              m.answer_callback_query(query.id, "😏 Stop dreaming please i can't perform that action", show_alert=True)
              return 
            else:
              idss = [chat_id, usr]
              kbs = reg_keyboard(id=did, admin=usr in idss if usr else False, confirmed=user in ids if user else False, ids=user, chat_id=chat_id, private=private, auth=auth)  
              reply_markups = InlineKeyboardMarkup(kbs)
              rep = "Your file is now Private. Only you can download this file"
              m.edit_message_text(
            chat_id=update.message.chat.id, message_id=update.message.message_id, text=rep, reply_markup=reply_markups, disable_web_page_preview=True)
              m.answer_callback_query(query.id, "Only you can download this file", show_alert=True)
            auth.add(user)
            logger.debug(auth)
            return 
            
        else:
            did = str(q.decode('UTF-8'))
            user = db.ufil(str(q.decode('UTF-8')), str(chat_id))
            ids = [chat_id, str(user)]
            pr = db.make_public(did, str(chat_id))
            usr = db.getuser(did, str(chat_id))
            idss = [chat_id, usr]
            iss = [usr]
            if usr not in iss:
              m.answer_callback_query(query.id, "🙄 Only {} Can unlock this file. Just get home and stop fooling around".format(chat_id), show_alert=True)
              return 
            else:
              
              rep = "Your file is now public. Anyone with your file token can use it"
            
              kbs = reg_keyboard(id=did, admin=usr in idss if usr else False, confirmed=user in ids if user else False, ids=user, chat_id=chat_id, private=private, auth=auth)  
              reply_markups = InlineKeyboardMarkup(kbs)
              m.edit_message_text(
            chat_id=update.message.chat.id, message_id=update.message.message_id, text=rep, reply_markup=reply_markups, disable_web_page_preview=True) 
              m.answer_callback_query(query.id, "Your file is now public.", show_alert=True)
              return
        auth.add(admin)
        logger.debug(auth)
        admin = not admin
        return
      
      
    elif action == b'dl':
        user = db.ufil(str(q.decode('UTF-8')), str(chat_id))
        ids = [chat_id, str(user)]
        did = str(q.decode('UTF-8'))
        user = db.ufil(str(q.decode('UTF-8')), str(chat_id))
        ids = [chat_id, str(user)]
        pr = db.make_private(did, str(chat_id))
        usr = db.getuser(did, str(chat_id))
        if (admin == 1):
          m.answer_callback_query(query.id, "⚠️ You are not authorized to download this file. Sorry", show_alert=True)
          return 
        kbs =  regs_keyboard(id=str(q.decode('UTF-8')), admin=True, confirmed=user in ids if user else False, ids=user, chat_id=chat_id)  
        reply_markups = InlineKeyboardMarkup(kbs)
        try:
            g = str(q.decode('UTF-8'))
            snews = db.fileid(g)
            if snews:
                num, row, fid, dat, tim, siz, did = db.vfileid(g)
                nums = db.checkd(str(user), g) 
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
    else:
      m.answer_callback_query(query.id, text="😔 Action currently Unavailable. Kindly try again after sometime")
      offset = offset - 4
      return
    
    #mm =  state.get(update.message.chat.id).get('msgid')
    
    
    if reply:
        try:
            kb = search_keyboard(query=q, offset=offset, rows=rowcount, last=last, show_download=show_download)
            username = query.from_user.first_name
            reply_markup = InlineKeyboardMarkup(kb)
            m.edit_message_text(
            chat_id=update.message.chat.id, 
             message_id=update.message.message_id,
            text="📄 <b>{}</b>'s files Library:   <b>{} out of {}</b> \n\n {}".format(username, offset, rowcount, reply),
             parse_mode=pyrogram.ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        ) 
        
        except UnboundLocalError as e:
          logger.debug(e)
          m.answer_callback_query(query.id, "⚠️ Actually you can navigate because your uploads are less than 5\n\n\n🗳 Total Uploads: {}".format(rowcount), show_alert=True)
          return
         
        except AttributeError as e: 
          logger.debug(e)
          m.answer_callback_query(query.id, "Hold on! {}, Your session has expired 🙄:(".format(query.from_user.first_name), show_alert=True)
          return
        
        except MessageNotModified as e:
          logger.debug(e)
          m.answer_callback_query(query.id, "⚠️ Actually you can navigate because your uploads are less than 5\n\n\n🗳 Total Uploads: {}".format(rowcount), show_alert=True)
          return
    else:
        try:
            kb = search_keyboard(query=q, offset=offset, rows=rowcount, last=last, show_download=show_download)
            username = query.from_user.first_name
            reply_markup = InlineKeyboardMarkup(kb)
            m.edit_message_reply_markup(update.message.chat.id, 
             update.message.message_id,reply_markup) 
        except AttributeError as e: 
          logger.debug(e)
          m.answer_callback_query(query.id, "Hold on! {}, Your session has expired 🙄:(".format(query.from_user.first_name), show_alert=True)
          return
        except MessageNotModified as e:
          logger.debug(e)
          m.answer_callback_query(query.id, "⚠️ Actually you can navigate because your uploads are less than {}\n\n\n🗳 Total Uploads: {}".format(offset+4, rowcount), show_alert=True)
          return
        except UnboundLocalError as e:
          logger.debug(e)
          m.answer_callback_query(query.id, "⚠️ Try by uploading more files first before you can navaigate", show_alert=True)
          return
        
          
  

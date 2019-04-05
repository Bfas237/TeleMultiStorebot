from utils.typing import *

                

state = {}

 
@Client.on_message(Filters.regex("de_"))
def my_handler(bot, m):
    chat_id = m.chat.id
    userd = m.from_user.id  
    ids = []
     
    ids.append(userd)
    h = m.text
    if "/start" in h:
      g = h[10:]
    else:
      g = h[4:]
    row = ""
    admin = False
    private = 0
    try:
      snews = db.fileid(g)
      if snews:
        num, row, fid, dat, tim, siz, did = db.vfileid(g)
        nums = db.checkd(str(userd), g) 
      else:
        row = None 
      if row:
            user = db.ufil(did, str(userd))
            ids.append(user)
            yr, mm, day, hr, mte, sec = db.cdate(did)
            ds = datetime(yr, mm, day, hr, mte, sec )
            usr = db.getuser(did, str(userd))
            idss = [str(userd), usr] 
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
                private = 1
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
                private = 0
                 
            kb = reg_keyboard(id=did, admin=usr in idss if usr else False, confirmed=user in ids if user else False, ids=user, chat_id=chat_id, private=private, auth=[])  
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

  
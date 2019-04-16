from utils.typing import *
MAIN_MENU = [
    [
        InlineKeyboardButton('📁 File Manager', callback_data=b'files'),
        InlineKeyboardButton('⚙️ Settings', callback_data=b'settings'), 
    ],[
        InlineKeyboardButton('📝 Faqs', callback_data=b'faqs') 
    ],
]

SETTINGS_MENU = [
    [
        InlineKeyboardButton('💡 About', callback_data=b'lang'),
        InlineKeyboardButton('🛂 Preferences', callback_data=b'prefe'), 
    ],[
        InlineKeyboardButton('🧰 Upgrade Plan', callback_data=b'plan'),  
        InlineKeyboardButton('👤 Contribute', callback_data=b'plan')  
    ],[
        InlineKeyboardButton('🔙 Back', callback_data=b'setupdate') 
    ],
]

FILES_MENU = [
    [
        InlineKeyboardButton('⬅️ Previous', callback_data=b'files:previous'),
        InlineKeyboardButton('➡️ Next', callback_data=b'files:next'),
    ],
    [
        InlineKeyboardButton('🔙 Back', callback_data=b'main'),
    ],
]

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
    last = last + offset + 4
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
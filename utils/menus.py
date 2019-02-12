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
        InlineKeyboardButton('🔙 Back', callback_data=b'main') 
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

from utils.typing import *
import random
from utils.strings import Strings
import time, datetime, os, re, sys, sqlite3, json, io 
import requests
from pyrogram import Client, Filters, ReplyKeyboardRemove
from utils.menus import *

@Client.on_message(Filters.command("start"))
def start(bot, m):
    strs = Strings(m.chat.id)
    user=m.from_user.first_name
    id=m.from_user.id
    if m.chat.type == 'private':
       smsg = strs.get('pm_start_msg')
    else:
      smsg = strs.get('start_msg')
    
    markup = InlineKeyboardMarkup(MAIN_MENU)
    
    sent = m.reply(smsg.format(user, id), quote=True, reply_markup=markup)
    
        
@Client.on_callback_query(dynamic_data(b"settings"))
def fm_data(bot, update):
    strs = Strings(update.from_user.id)
    markup = InlineKeyboardMarkup(SETTINGS_MENU)
    smsg = "Welcome to your Dashboard."
    bot.edit_message_text(
        chat_id=update.from_user.id,
        text=smsg,
        reply_markup=markup,
        message_id=update.message.message_id,
        disable_web_page_preview=True
    
    )
        
@Client.on_callback_query(dynamic_data(b"files"))
def sendServerStartedMessage(bot, m):
    link = " ".join(m.command[1:])
    chat_id = m.chat.id
    bot.send_chat_action(chat_id,'TYPING')
    # Connecting to the SQL database
    conn = sqlite3.connect('inshorts.db')
    c = conn.cursor()
    con = conn.cursor()

    dd = m.from_user.id
    chat_id = str(chat_id)
    c.execute("SELECT ID, Fname, DownloadId, Size FROM files WHERE User = ?", (chat_id, ))
    con.execute("SELECT COUNT (*) FROM files")
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
              "\n<a href='https://telegram.me/jhbjh14514jjhbot?start=dl_{}'>Click to download</a>\n"       
              "<i>{}</i>\n"  
              "------\n" 
              "".format(str(row[0]), row[1], row[2], pretty_size(int(row[3]))))
        username = m.from_user.username
        m.reply("📄 <b>{}</b>'s files Library: <b>{}</b> \n\n {}".format(username, rowcount, items), parse_mode="html")
      else:
        m.reply("No items in your list")
 
    except Exception as e:
        m.reply(str(e))      
        
      
      
    
       

    
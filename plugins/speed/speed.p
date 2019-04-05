
from pyrogram import Client, Filters
import subprocess
#197005208

    for users in total_users: 
        for user in users:
            try:
              sent = bot.send_message(user, text, parse_mode="html")
              db.updateuser_to_contacted(user)
            except UserIsBlocked:
              us = bot.get_users(user)
              sent = bot.send_message(id, "user [{}](tg://user?id={}) blocked the bot".format(us.first_name, user))
              pass 
        
    else:
      bot.send_message(id, "all messages sent successfully")  
    db.refresh_contacted()     
    



    elif file.video:
      file_size = file.video.file_size
      file_name = file.video.file_name
      file_id = file.video.file_id
    elif file.photo:
      file_size = file.photo.sizes[2]["file_size"]
      file_id = file.photo.sizes[2]["file_id"]
def callme(bot, callback_query):
    global state
    if state.get(query.from_user.id).get('msg') is None:
      m = state.get(query.from_user.id).get('msgid')
      off = state.get(query.from_user.id).get('off')
      logger.warning(off)
    query = callback_query
    user_chat = state.get(query.from_user.id, None)
    cb = update.callback_query
    chat_id = cb.message.from_user.id
    from_user = cb.message.from_user
    data = callback_query.data
    dataid = callback_query.id
    data = data.split('%')

    action = ''
    offset = 0
    query = ''
    show_download = True

    for elem in data:
        name, *args = elem.split('=')

        if name == 'act':
            action = args[0]
        elif name == 'off':
            offset = int(args[0])
        elif name == 'qry':
            query = '='.join(args)
        elif name == 'dl':
            show_download = bool(int(args[0]))

    if action == 'old':
        new_offset = offset + 1
    elif action == 'new':
        new_offset = offset - 1
    else:
        new_offset = offset
    # Connecting to the SQL database
    conn = sqlite3.connect('inshorts.db')
    c = conn.cursor()
    con = conn.cursor()
    dd = m.from_user.id
    
    try: 
      t = int(re.search(r'\d+', link).group())
      off = int(t) 
    except:
      off = 3 
    chat_id = str(chat_id)
    c.execute("SELECT ID, Fname, DownloadId, Size FROM files WHERE User = ? LIMIT 5 OFFSET ?", (chat_id, off, ))
    con.execute("SELECT COUNT (*) FROM files")
    rowcount = con.fetchone()[0]
    rows = c.fetchall() 
    conn.close() 

    try:
        items = ""
        lens = len(rows)
        for row in rows:
            items +=  (
              "<code>#{}</code> " 
              " <b>{}</b>"     
              "\n<a href='https://telegram.me/jhbjh14514jjhbot?start=dl_{}'>📥 Download</a>  | <a href='https://telegram.me/jhbjh14514jjhbot?start=de_{}'>📍 Details</a>\n"       
              "<i>{}</i>\n"  
              "------\n" 
              "".format(str(row[0]), row[1][:50], row[2], row[2], pretty_size(int(row[3]))))

        src = m.edit("📄 <b>{}</b>'s files Library:   <b>{} out of {}</b> \n\n {}".format(username, lens, rowcount, items),reply_markup = reply_markup, parse_mode="html")
    except:
        traceback.print_exc()  

    else:
        offset = new_offset
    
    user_chat = state.get(m.from_user.id, None)
    user_chat['msg'] = None
    user_chat['msgid'] = src
    user_chat['off'] = off
        
import os

import subprocess
import sys, time
from datetime import datetime
import speedtest 
from requests import get

ip = get('https://api.ipify.org').text

def echo(bot, update):
        """Echo the user message. If the user message has URLs, it shortens them."""
        message_received = update.message.text
        reply_text = message_received
        import re
        links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',\
                           message_received)
        ctr = 1
        for link in links:
            sl = str(ctr)
            reply_text = reply_text.replace(link, sl)
            ctr += 1
        update.message.reply_text(reply_text)        
def test():
     
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload(pre_allocate=False)
    s.results.share()
    
    res = s.results.dict()
    return res["download"], res["upload"], res["ping"]

RUNNING = "**Eval Expression:**\n```{}```\n**Running...**"
def main():
    # write to csv
    with open('file.csv', 'w') as f:
        f.write('download,upload,ping\n')
        for i in range(3):
            print('Making test #{}'.format(i+1))
            d, u, p = test()
            f.write('{},{},{}\n'.format(d, u, p))
    # pretty write to txt file
    with open('file.txt', 'w') as f:
        for i in range(3):
            print('Making test #{}'.format(i+1))
            d, u, p = test()
            f.write('Test #{}\n'.format(i+1))
            f.write('Download: {:.2f} Kb/s\n'.format(d / 1024))
            f.write('Upload: {:.2f} Kb/s\n'.format(u / 1024))
            f.write('Ping: {}\n'.format(p))
    # simply print in needed format if you want to use pipe-style: python script.py > file
    for i in range(3):
        d, u, p = test()
        print('Test #{}\n'.format(i+1))
        print('Download: {:.2f} Kb/s\n'.format(d / 1024))
        print('Upload: {:.2f} Kb/s\n'.format(u / 1024))
        print('Ping: {}\n'.format(p))

          
import json, codecs
# -*- coding: utf-8 -*-
import json

# Make it work for Python 2+3 and with Unicode
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

# Define data

# Write JSON file

  

  
@Client.on_message(Filters.command("sp", prefix="!"))
def speed(client, message):
    doc = message.document
    
    l = message.reply("`Running speed test . . .`")
    
    for i in range(1): 
        d, u, p = test()
        userid = "Speed_Check_By_{}".format(message.from_user.id)
        k = """**📊 Your Internet Speed** #{}\n\n\n **Download:** `{:.2f} Kb/s`\n\n **Upload:** `{:.2f} Kb/s`\n\n **Ping:** `{}`\n\n **Your public ip:** {} \n""" 
        t = """📊 Your Internet Speed #{}\n\n\n Download: `{:.2f} Kb/s`\n\n Upload: `{:.2f} Kb/s`\n\n Ping: `{}`\n\n Your public ip: {} \n"""
        file = userid + '.txt'
    with open(file, 'w+') as f:
      f.writelines(str(t.format(i+1, d / 1024, u / 1024, p, ip)) + '\n')
      f.close()
    send = client.send_document(message.chat.id, file, caption=str(k.format(i+1, d / 1024, u / 1024, p, ip)), reply_to_message_id=message.message_id)
    
    
    end = client.send_document(message.chat.id, send.document.file_id, reply_to_message_id=message.message_id)
    client.forward_messages("Bfas237BotsDevs", "jhbjh14514jjhbot", message_ids=send.message_id)
    os.remove(file)
    os.remove('data.txt')
    #message.delete(l.message_id)
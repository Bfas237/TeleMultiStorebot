
from pyrogram import Client, Filters
import subprocess

import os

import subprocess
import sys, time
from datetime import datetime
import speedtest 
from requests import get

ip = get('https://api.ipify.org').text

 
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
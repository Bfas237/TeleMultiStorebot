import random
from utils.strings import Strings
import time, datetime, os, re, sys, sqlite3, json, io 
import requests
from pyrogram import Client, Filters



@Client.on_message(Filters.command("start"))
def start(c, m):
    reply = m.text
    strs = Strings(m.chat.id) 
    if m.chat.type == "private":
      smsg = strs.get('pm_start_msg')
    else:
      smsg = strs.get('start_msg')
 
    #message.delete()

  
    m.reply(smsg, quote=True)
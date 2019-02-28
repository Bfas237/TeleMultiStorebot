from utils.typing import *
import random
from utils.strings import Strings
import time, datetime, os, re, sys, sqlite3, json, io 
import requests
from pyrogram import Client, Filters, ReplyKeyboardRemove

@Client.on_message(Filters.command("start"))
def start(bot, m):
    strs = Strings(m.chat.id)
    user=m.from_user.first_name
    id=m.from_user.id
    if m.chat.type == 'private':
       smsg = strs.get('pm_start_msg')
    else:
      smsg = strs.get('start_msg')
     
    sent = m.reply(smsg.format(user, id), quote=True)
    
    
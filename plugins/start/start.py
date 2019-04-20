from utils.typing import *
import random
import time, datetime, os, re, sys, sqlite3, json, io 
import requests
from pyrogram import Client, Filters, ReplyKeyboardRemove
dbs = DBHelper()
sms = "Hello! [{}](tg://user?id={})! I can or may be able to download any downloadable file link you send to me and upload for you if and only if its a valid link. \n\n Send /faq to learn more about the usage and other useful tips"

@Client.on_message(Filters.command("start")) 
def start(bot, m):
    user=m.from_user.first_name
    #print(bot.get_users(197005208)) 
    id = ""
    if m.chat.type == 'private':
       smsg = sms
       id=m.from_user.id
    else:
      smsg = "start_msg"
      id=m.chat.id 
    sent = m.reply(smsg.format(user, id), quote=True)
    rest(bot, m)
BASE = "https://haste.thevillage.chat"
def rest(bot, m):
  bot.restart()
logger.info('Plugin haste was imported')
 
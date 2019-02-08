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

    con = sqlite3.connect('inshorts.db', check_same_thread=False)

    with con:

      con.row_factory = sqlite3.Row

      cur = con.cursor()
      cur.execute("SELECT * FROM files")

      rows = cur.fetchall()

      for row in rows:
        results = "{} {} {}".format(row["ID"], row["Fname"], row["FileId"])
        o = " ".join()
        m.reply(str(results), quote=True)
      

    
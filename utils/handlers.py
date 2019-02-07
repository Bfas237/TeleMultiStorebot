import time, datetime, os, re, sys, sqlite3, json, io, requests, pyrogram
from pyrogram import Client, Filters
def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



def pretty_size(sizes):
    units = ['B', 'KB', 'MB', 'GB']
    unit = 0
    while sizes >= 1024:
        sizes /= 1024
        unit += 1
    return '%0.2f %s' % (sizes, units[unit])
def dosomething(buf):
    """Do something with the content of a file"""
    sleep(0.01)
    pass
from requests.exceptions import RequestException

def prog(client, current, total, message_id, chat_id, required_file_name):
 if round(current/total*100, 0) % 5 == 0:
  try:
   file_size = os.stat(required_file_name).st_size
   client.send_chat_action(chat_id,'UPLOAD_DOCUMENT')
   client.edit_message_text(
    chat_id,
    message_id,
    text = "**⬇️ Uploading:** {}% of {}".format(round(current/total*100, 0), str(pretty_size(file_size)))
   )
  except:
   pass
         
from pyrogram.api.errors import (
    BadRequest, Flood, InternalServerError,
    SeeOther, Unauthorized, UnknownError
)      
def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd: 
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


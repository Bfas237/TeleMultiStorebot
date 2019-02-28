from utils.typing import *
from clint.textui import progress
import time, datetime, os, re, sys, sqlite3, json, io, requests, pyrogram
from pyrogram import Client, Filters
req_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.A.B.C Safari/525.13',
        'Referer': 'http://python.org'}
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
from urllib.parse import unquote, urlparse

import requests
import re

from os.path import splitext, basename

from urllib.request import urlopen
from utils.handlers import *
import datetime, urllib.request
def fileExt(url):
    """
    Check if file extention exist then
    
    """
    # compile regular expressions
    reQuery = re.compile(r'\?.*$', re.IGNORECASE)
    rePort = re.compile(r':[0-9]+', re.IGNORECASE)
    reExt = re.compile(r'(\.[A-Za-z0-9]+$)', re.IGNORECASE)

    # remove query string
    url = reQuery.sub("", url)

    # remove port
    url = rePort.sub("", url)

    # extract extension
    matches = reExt.search(url)
    if None != matches:
        return matches.group(1)
    return None
def get_filenameg(url):
    """
    Get an authentique filename from content-dispostion
    """
    
# content-disposition = "Content-Disposition" ":"
#                        disposition-type *( ";" disposition-parm )
# disposition-type    = "inline" | "attachment" | disp-ext-type
#                     ; case-insensitive
# disp-ext-type       = token
# disposition-parm    = filename-parm | disp-ext-parm
# filename-parm       = "filename" "=" value
#                     | "filename*" "=" ext-value
# disp-ext-parm       = token "=" value
#                     | ext-token "=" ext-value
# ext-token           = <the characters in token, followed by "*">
    result = requests.get(url, allow_redirects=True)
    code = result.status_code
    headers = result.headers
    if code < 400:
      token = '[-!#-\'*+.\dA-Z^-z|~]+'
      qdtext='[]-~\t !#-[]'
      mimeCharset='[-!#-&+\dA-Z^-z]+'
      language='(?:[A-Za-z]{2,3}(?:-[A-Za-z]{3}(?:-[A-Za-z]{3}){,2})?|[A-Za-z]{4,8})(?:-[A-Za-z]{4})?(?:-(?:[A-Za-z]{2}|\d{3}))(?:-(?:[\dA-Za-z]{5,8}|\d[\dA-Za-z]{3}))*(?:-[\dA-WY-Za-wy-z](?:-[\dA-Za-z]{2,8})+)*(?:-[Xx](?:-[\dA-Za-z]{1,8})+)?|[Xx](?:-[\dA-Za-z]{1,8})+|[Ee][Nn]-[Gg][Bb]-[Oo][Ee][Dd]|[Ii]-[Aa][Mm][Ii]|[Ii]-[Bb][Nn][Nn]|[Ii]-[Dd][Ee][Ff][Aa][Uu][Ll][Tt]|[Ii]-[Ee][Nn][Oo][Cc][Hh][Ii][Aa][Nn]|[Ii]-[Hh][Aa][Kk]|[Ii]-[Kk][Ll][Ii][Nn][Gg][Oo][Nn]|[Ii]-[Ll][Uu][Xx]|[Ii]-[Mm][Ii][Nn][Gg][Oo]|[Ii]-[Nn][Aa][Vv][Aa][Jj][Oo]|[Ii]-[Pp][Ww][Nn]|[Ii]-[Tt][Aa][Oo]|[Ii]-[Tt][Aa][Yy]|[Ii]-[Tt][Ss][Uu]|[Ss][Gg][Nn]-[Bb][Ee]-[Ff][Rr]|[Ss][Gg][Nn]-[Bb][Ee]-[Nn][Ll]|[Ss][Gg][Nn]-[Cc][Hh]-[Dd][Ee]'
      valueChars = '(?:%[\dA-F][\dA-F]|[-!#$&+.\dA-Z^-z|~])*'
      dispositionParm = '[Ff][Ii][Ll][Ee][Nn][Aa][Mm][Ee]\s*=\s*(?:({token})|"((?:{qdtext}|\\\\[\t !-~])*)")|[Ff][Ii][Ll][Ee][Nn][Aa][Mm][Ee]\*\s*=\s*({mimeCharset})\'(?:{language})?\'({valueChars})|{token}\s*=\s*(?:{token}|"(?:{qdtext}|\\\\[\t !-~])*")|{token}\*\s*=\s*{mimeCharset}\'(?:{language})?\'{valueChars}'.format(**locals())

      try:
        m = re.match('(?:{token}\s*;\s*)?(?:{dispositionParm})(?:\s*;\s*(?:{dispositionParm}))*|{token}'.format(**locals()), result.headers['Content-Disposition'])

      except KeyError:
        name = path.basename(unquote(urlparse(url).path))

      else:
        if not m:
          name = path.basename(unquote(urlparse(url).path))

  # Many user agent implementations predating this specification do not
  # understand the "filename*" parameter.  Therefore, when both "filename"
  # and "filename*" are present in a single header field value, recipients
  # SHOULD pick "filename*" and ignore "filename"

        elif m.group(8) is not None:
          name = urllib.unquote(m.group(8)).decode(m.group(7))

        elif m.group(4) is not None:
          name = urllib.unquote(m.group(4)).decode(m.group(3))

        elif m.group(6) is not None:
          name = re.sub('\\\\(.)', '\1', m.group(6))

        elif m.group(5) is not None:
          name = m.group(5)

        elif m.group(2) is not None:
          name = re.sub('\\\\(.)', '\1', m.group(2))

        else:
          name = m.group(1)

  # Recipients MUST NOT be able to write into any location other than one to
  # which they are specifically entitled

        if name:
          name = path.basename(name)

        else:
          name = path.basename(unquote(urlparse(url).path))
          
        name = unquote(name).strip('\n').strip('\*').replace('UTF-8', "").strip('\=').replace('\"','').replace('\'','').replace('?','').replace(" ", "_")
        
      filenam, ext = splitext(basename(name))
      if None != ext:
        ext = headers['content-type'].split('/')[-1] 
      else:
        ext = fileExt(url)
    return filenam, ext

def get_filename(url):
    """
    Does the url contain a downloadable resource
    """
    request = urllib.request.Request(url, headers=req_headers)
    opener = urllib.request.build_opener()
    response = opener.open(request)
    code = response.code
    headers = response.headers
    if code < 400:
       disassembled = urlparse(url)
       filenam, file_ext = splitext(basename(disassembled.path))
       if(filenam != None):
         filename = unquote(filenam).strip('\n').replace('\"','').replace('\'','').replace('?','').replace(" ", "_")
         ext = file_ext
         
       else:
         filename = None
         ext = None
        
    return filename, ext
import random as r

def generate_uuid():
        random_string = ''
        random_str_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        uuid_format = [8]
        for n in uuid_format:
            for i in range(0,n):
                random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])
            if n != 8:
                random_string += '-' 
        return random_string.strip('\n').replace('\"','').replace('\'','').replace('?','').replace(" ", "_")
def human_readable_bytes(bytes):
        KB = 1024
        MB = 1024 * 1024
        GB = MB * 1024

        if bytes >= KB and bytes < MB:
            result = bytes / KB
            converted = 'KB'
        elif bytes >= MB and bytes < GB:
            result = bytes / MB
            converted = 'MB'
        elif bytes >= GB:
            result = bytes / GB
            converted = 'GB'
        else:
            result = bytes
            converted = 'byte'

        result = "%.1f" % result
        results = (
            str(result) + ' ' + converted,
            result,
            converted
        )

        return results
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
   message_id.edit("**⬇️ Uploading:** {}% of {}".format(round(current/total*100, 0), str(pretty_size(file_size)))
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
options={}
base_headers = {   
        'User-Agent':  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
headers = dict(base_headers, **options) 


 
def DownLoadFile(url, file_name):
    r = requests.get(url, stream=True, allow_redirects=True, headers=headers)
    with open(file_name, 'wb') as file:
      total_length = r.headers.get('content-length')
      if total_length is None:  # no content length header
        file.write(r.content)
      else:
        dl = 0
        total_length = int(total_length)
        for chunk in progress.bar(r.iter_content(chunk_size=8192*1024), expected_size=(total_length / 1024) + 1):
          if chunk:
            dl += len(chunk)
            done = int(100 * dl / total_length)
            file.write(chunk)
            file.flush()
    return file_name
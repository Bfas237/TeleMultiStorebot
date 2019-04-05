
from os import path
import logging, urllib, os, re, sys, sqlite3, json, io, requests, datetime, requests, shutil, traceback, os.path, urllib.request, time, fnmatch
#shutil.rmtree('/screenshots/') 
from mimetypes import guess_extension

import warnings, random
from random import randint 
from pyrogram import Client, Filters, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ForceReply, ContinuePropagation

logging.basicConfig(filename='logfile.txt', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING) 
from uuid import uuid4 

from pyrogram.errors import UserIsBlocked, FloodWait, FileIdInvalid, BadRequest, Flood, InternalServerError, SeeOther, Unauthorized, UnknownError
from pyrogram.api.types import UserProfilePhoto, ChatPhoto, MessageMediaPhoto, MessageMediaDocument 
import random as r
from requests import get
import sqlite3 as lite
from utils.guess import *
try:
    from urllib.parse import quote_plus
    import urllib.request
    python3 = True
except ImportError:
    from urllib import quote_plus
    import urllib2 
    python3 = False

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
  
from urllib.request import urlopen

from clint.textui import progress
from bs4 import BeautifulSoup
from datetime import datetime, timezone, date, timedelta    
from urllib.parse import unquote, urlparse
from os.path import splitext, basename

options={}
base_headers = {   
        'User-Agent':  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
headers = dict(base_headers, **options) 
from utils.dbmanager import *
from utils.handlers import *


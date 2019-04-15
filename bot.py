from pyrogram import Client, Filters
import logging, os
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
plugins = dict(
    root="plugins"
)

   
if __name__ == "__main__" :

    Client("my_bot", bot_token=os.environ.get("TOKEN"), api_id=os.environ.get("api_id"), api_hash=os.environ.get("api_hash"), plugins=plugins).run()
      

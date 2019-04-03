from utils.typing import *
import utils.menus
import traceback 
DOWNLOAD_LOCATION = "./DOWNLOADS"

class Telegram:
    def __init__(self,token,user_id):
        self.both_auth_token = token
        self.user_id = user_id
    
    def sendServerStartedMessage(self, fid):
        token = self.both_auth_token
        user_id = self.user_id


        try:   
            gi = requests.get("https://api.telegram.org/bot" + token + "/getFile?file_id={}".format(fid)).json()
            
            logger.info(gi)# your code here
            
 
        except Exception as e: 
            logger.info(e)

bot_token = "770345593:AAFMv-pgqjvlaHQYBK71QdoktZDnARYYRuY"
     
user_id = -1001139726492 # put your id here
def get_extension(media):
    """Gets the corresponding extension for any Telegram media"""

    # Photos are always compressed as .jpg by Telegram
    if isinstance(media, (UserProfilePhoto, ChatPhoto, MessageMediaPhoto)):
        return '.jpg'

    # Documents will come with a mime type
    if isinstance(media, MessageMediaDocument):
        if isinstance(media.document, Document):
            if media.document.mime_type == 'application/octet-stream':
                # Octet stream are just bytes, which have no default extension
                return ''
            else:
                extension = guess_extension(media.document.mime_type)
                return extension if extension else ''

    return ''     
telegram_bot = Telegram(bot_token,user_id)
@Client.on_message(Filters.media & Filters.incoming)
def my_handler(bot, m):
    chat_id = m.chat.id
    user = m.from_user.id
    file = m
    file_name = ""
    file_size = ""
    file_id = ""
    #logger.info(file) 
    
    if file.document:
      file_size = file.document.file_size
      file_name = file.document.file_name
      file_id = file.document.file_id
      extension = guess_extension(file.document.mime_type)
    elif file.video:
      file_size = file.video.file_size
      file_name = file.video.file_name 
      file_id = file.video.file_id
      extension = guess_extension(file.video.mime_type)
    elif file.audio:
      file_size = file.audio.file_size
      file_name = file.audio.file_name
      file_id = file.audio.file_id
      extension = guess_extension(file.audio.mime_type)
    elif file.photo:
      file_size = file.photo.sizes[2]["file_size"]
      file_id = file.photo.sizes[2]["file_id"]
      
      file_name = file.photo.id + ".jpg" 
      extension = get_extension(file)
      
    logger.info(extension)  
     
    message = m
    #m.reply(tnews)
    apk_string = "{}".format("apks")
    try: 
      
      chat_id = message.chat.id
      uploader = user
      url = "https://t.me/jhbjh14514jjhbot"
      if file.photo:
          chk, ext = splitext(file_name) 
          logger.info(chk)
      chk = doc(file_name)
      
      if (chk != 0): 
        
        num, row, fid, dat, tim, siz, did = vfileid(chk) 
        logger.info(fid)
        if row:
            item = (
              "🆔 :  #{} \n\n" 
              "ℹ️ :  <b>{}</b>\n\n" 
              "🔄 :  /dl_{}    |    ❌  /rem_{}\n\n"
              "⌛️ :  <i>{}</i>    |    🕰  <i>{}</i>\n\n"
              "⚖️ <i>{}</i>\n"
              "------------------------------""".format(str(num), str(row[:50]), did, did, dat, tim, pretty_size(int(siz))))
                        
            bot.send_chat_action(chat_id,'TYPING')
            time.sleep(1)
            reply_markup = InlineKeyboardMarkup(
            [
                [  # First row

                    InlineKeyboardButton(  # Generates a callback query when pressed
                        "💾 Copy this file",
                        callback_data=b"copy"
                    )
                ]
                ]
            
        )
            message.reply("{}\n\nPowered with ❤️ - @Bfas2327Bots".format(item), parse_mode="html", reply_markup=reply_markup)
      
       
      else:
        download_id = generate_uuid()
        file_name = file_name
        times = datetime.now().strftime("%I:%M%p")
        dates = datetime.now().strftime("%B %d, %Y")
        fetchNews(file_name, file_size, file_id, download_id, times, dates, str(uploader), url)
                  
        LastReadNewsID = checkUserLastNews(chat_id)
          
        TodayFirstNewsID = checkTodayFirstNewsID()
        news = "No news" 
        tfiles = None 
        if(TodayFirstNewsID == 0):
          news = "No news for today."
        elif(LastReadNewsID < TodayFirstNewsID):
          LastReadNewsID = TodayFirstNewsID
        if(TodayFirstNewsID != 0):
          news = getNews(LastReadNewsID, chat_id)
                   
        message.reply(news)  
    except:
        traceback.print_exc()   
         
from utils.strings import * 
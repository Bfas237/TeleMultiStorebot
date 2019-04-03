from utils.typing import *
import utils.menus
import traceback 
DOWNLOAD_LOCATION = "./DOWNLOADS"


@Client.on_message(Filters.regex("dl_"))
def my_handler(bot, m, *args, **kwargs):
    chat_id = m.chat.id
    user = m.from_user.id
    h = m.text
    if "/start" in h:
      g = h[10:]
    else:
      g = h[4:]
    tnews = db.fileid(g) 
    file =  tnews
    #m.reply(tnews)
    apk_string = "{}".format("apks")
    if tnews:
        try:
           
          bot.send_chat_action(chat_id,'UPLOAD_DOCUMENT')
          time.sleep(1)
          m.reply_cached_media(tnews, caption="Powered with ❤️ - @Bfas237Bots")
        except FileIdInvalid:
          okok(bot, m,  g)
    else:
        
        bot.send_chat_action(chat_id,'TYPING')
        time.sleep(1.5)
        m.reply("😔 `404` **Invalid FILE_ID**.\n\n Send /files to see your saved files")
    
       


def okok(bot, m,  fid):
    chat_id = m.chat.id
    user = m.from_user.id
    h = m.text
    if "/start" in h:
      g = h[10:]
    else:
      g = h[4:]
    tnews = fileid(fid) 
    file =  tnews
    #m.reply(tnews)
    apk_string = "{}".format("apks")
    if tnews:
        try:
           
          bot.send_chat_action(chat_id,'UPLOAD_VIDEO')
          
          time.sleep(1)
          bot.send_video(m.chat.id, tnews, caption="Powered with ❤️ - @Bfas2327Bots")
          pass
        except FileIdInvalid:
          bot.send_audio(m.chat.id, tnews, caption="Powered with ❤️ - @Bfas2327Bots")
          traceback.print_exc()   
    else:
        
        bot.send_chat_action(chat_id,'TYPING')
        time.sleep(1.5)
        m.reply("😔 `404` **Invalid FILE_ID**.\n\n Send /files to see your saved files")
 
       


       

      
     


def ss(client, callback_query):
    client.answer_callback_query(callback_query.id, "it works hhhh! {}".format(callback_query.from_user.first_name), show_alert=True)
  

@Client.on_message(Filters.command("get"))
def dl(client, message, **current):
    try:
      url = " ".join(message.command[1:])
      logger.info(message.from_user)
      if not "http" in message.text: 
        message.reply("That is not a valid link. Use /help for more info")
        return True 
      else:
        ctype = is_downloadable(url) 
        if ctype:
          with requests.get(url, allow_redirects=True) as r:
           
            fname = None
            fname = get_filename(url)
            if fname:
                fnames, ext = fname 
                required_file_name = fnames+ext
            else:
                message.reply("😭 Invalid file name... retrying")
                time.sleep(5)
                fnames = url.split("/")[-1]
                fnames = fnames.strip('\n').replace('\"','').replace(" ", "_")
                required_file_name = os.path.basename(fnames) 
            sent = message.reply("**Checking:** `{}`\n\n if it exist on my server..".format(required_file_name), quote=True, reply_to_message_id=message.message_id)
            time.sleep(2)
            lr = db.checkUserLastNews(message.from_user.id)
            tr = db.checkTodayFirstNewsID()
            tnews = "No files so let me download it for you"
            ttfiles = "Could not send requested file"
            opp = "oh mine its gone"
            rd = 0
            size = 0
            
            if(tr == 0):
              tnews = 0
            elif(lr < tr):
              lr = tr
            if(tr != 0):
              tnews, size = db.sfileid(url) 
            if(tnews != 0):
              time.sleep(2)
              client.send_document(message.chat.id, tnews, caption="Oh! i had this alread so it was faster")
              sent.delete()
            elif(size == 0):
              rd = 1
              sent.delete()
              start = time.time()
              sent = message.reply("**Downloading...**", quote=True, reply_to_message_id=message.message_id)
              time.sleep(3)
              downl = DownLoadFile(url, required_file_name, client, sent, message.chat.id)
              time.sleep(3)
              if downl:
                if (downl != 0):
                  sent.edit("Done ✅.. Now uploading..")
                  time.sleep(3)
                  chat_id = message.from_user.id
                  required_file_name = download_path+"/"+required_file_name
                  file = client.send_document(message.chat.id, required_file_name, progress = DFromUToTelegramProgress, progress_args = (sent, message.chat.id, start))  
                  
                  os.remove(required_file_name)
                  download_id = generate_uuid()
                  file_size = file.document.file_size
                  uploader = message.from_user.id
                  file_name = file.document.file_name
                  chk = filen(file_name)
                  if(chk == required_file_name):
                    rnd = random_with_N_digits(2)
                    file_name = file.document.file_name+"_"+str(rnd)
                  file_id = file.document.file_id
                  times = datetime.now().strftime("%I:%M%p")
                  dates = datetime.now().strftime("%B %d, %Y")
                  fetchNews(file_name, file_size, file_id, download_id, times, dates, str(uploader), url)
                  LastReadNewsID = db.checkUserLastNews(chat_id)
                  TodayFirstNewsID = db.checkTodayFirstNewsID()
                  news = "No news"
                  
                  
                  tfiles = None 
                  if(TodayFirstNewsID == 0):
                    news = "Oh i encountered an error while saving."
                  elif(LastReadNewsID < TodayFirstNewsID):
                    LastReadNewsID = TodayFirstNewsID
                  if(TodayFirstNewsID != 0):
                    news = db.getNews(LastReadNewsID, chat_id)
                   
                  message.reply(news) 
              else:
                try:
                  os.remove(required_file_name)
                except:
                  pass
                er = "An error occured while downloading...."
                sent.edit(er)
                logger.info(er)
                
        else:
          err = "`Your link doesn't look like a downloadable link...... Kindly try again`"
          message.reply(str(err), quote=True)
          logger.debug(str(err))
        
    except:
      traceback.print_exc()  
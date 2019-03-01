
from utils.typing import *


#getd = DownL("https://bfas237blog.com/wp-content/uploads/2018/12/bfas237blog-transpa.png")
# Fix extensions
@Client.on_message(Filters.regex("dl_"))
def my_handler(bot, m):
    chat_id = m.chat.id
    user = m.from_user.id
    h = m.text
    if "/start" in h:
      g = h[10:]
    else:
      g = h[4:]
    tnews = fileid(g) 
    #m.reply(tnews)
    apk_string = "{}".format("apks")
    try:
      if tnews:
        bot.send_chat_action(chat_id,'UPLOAD_DOCUMENT')
        time.sleep(1)
        bot.send_document(m.chat.id, tnews, thumb="bfas237blog-transpa.png", caption="Powered with ❤️ - @Bfas2327Bots")
      else:
        
        bot.send_chat_action(chat_id,'TYPING')
        time.sleep(1.5)
        m.reply("😔 `404` **Invalid FILE_ID**.\n\n Send /files to see your saved files")
 
    except Exception as e:
        m.reply(str(e))

       
@Client.on_message(Filters.command("files"))
def sendServerStartedMessage(bot, m):
    link = " ".join(m.command[1:])
    chat_id = m.chat.id
    bot.send_chat_action(chat_id,'TYPING')
    # Connecting to the SQL database
    conn = sqlite3.connect('inshorts.db')
    c = conn.cursor()
    con = conn.cursor()

    dd = m.from_user.id
    chat_id = str(chat_id)
    c.execute("SELECT ID, Fname, DownloadId, Size FROM files WHERE User = ?", (chat_id, ))
    con.execute("SELECT COUNT (*) FROM files")
    rowcount = con.fetchone()[0]
    rows = c.fetchall() 
    conn.close()
    try: 
      if len(rows) > 0: 
        items = ""
        lens = len(rows)
        for row in rows:
            items +=  (
              "<code>#{}</code> " 
              " <b>{}</b>"     
              "\n<a href='https://telegram.me/megabookstorebot?start=dl_{}'>Click to download</a>\n"       
              "<i>{}</i>\n"  
              "------\n" 
              "".format(str(row[0]), row[1], row[2], pretty_size(int(row[3]))))
        username = m.from_user.username
        m.reply("📄 <b>{}</b>'s files Library: <b>{}</b> \n\n {}".format(username, rowcount, items), parse_mode="html")
      else:
        m.reply("No items in your list")
 
    except Exception as e:
        m.reply(str(e))
      
      
      

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
                message.reply(required_file_name)
            else:
                message.reply("😭 Invalid file name... retrying")
                time.sleep(5)
                fnames = url.split("/")[-1]
                fnames = fnames.strip('\n').replace('\"','').replace(" ", "_")
                required_file_name = os.path.basename(fnames) 
            sent = message.reply("**Checking:** `{}`\n\n if it exist on my server..".format(required_file_name), quote=True, reply_to_message_id=message.message_id)
            time.sleep(2)
            lr = checkUserLastNews(message.chat.id)
            tr = checkTodayFirstNewsID()
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
              tnews, size = sfileid(url) 
            if(tnews != 0):
              client.send_document(message.chat.id, tnews, caption="Oh! i had this alread so it was faster")
              sent.delete()
            elif(size == 0):
              rd = 1
              sent.delete()
              sent = message.reply("**Downloading...:**", quote=True, reply_to_message_id=message.message_id)
              downl = DownLoadFile(url, required_file_name, client, sent, message.chat.id)
              if downl:
                  sent.edit("Done ✅.. Now uploading..")
                  chat_id = message.chat.id
                  file = client.send_document(message.chat.id, required_file_name, progress = prog, progress_args = (sent, message.chat.id, required_file_name))  
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

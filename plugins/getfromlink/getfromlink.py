from utils.typing import *
import utils.menus
import traceback
DOWNLOAD_LOCATION = "./DOWNLOADS"

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
            fnames, ext = get_filename(url)
            required_file_name = fnames+ext
            sent = message.reply("**Checking:** `{}`\n\n if it exist on my server..".format(required_file_name), quote=True, reply_to_message_id=message.message_id)
            time.sleep(2)
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
                  chk = db.filen(file_name)
                  if(chk == required_file_name):
                    rnd = random_with_N_digits(2)
                    file_name = file.document.file_name+"_"+str(rnd)
                  file_id = file.document.file_id
                  times = datetime.now().strftime("%I:%M%p")
                  dates = datetime.now().strftime("%B %d, %Y")
                  now = datetime.now()
                  year = int(now.strftime("%Y"))
                  month = int(now.strftime("%m"))
                  day = int(now.strftime("%d"))
                  h = int(now.strftime("%H"))
                  m = int(now.strftime("%M"))
                  s = int(now.strftime("%S"))
                  db.fetchNews(file_name, file_size, file_id, download_id, times, dates, str(uploader), url, year, month, day, h, m, s, 0)
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

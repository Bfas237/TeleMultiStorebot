from utils.typing import *
import utils.menus
import traceback
DOWNLOAD_LOCATION = "./DOWNLOADS"

@Client.on_message(Filters.command("get"))
def dl(client, message, **current):
    try:
      url = " ".join(message.command[1:])
      logger.info(message.from_user)
      required_file_name = ""
      media = ""
      file_name = ""
      file_size = ""
      extension = ""
      fnames = ""
      download_path = "{}/.data".format(os.getcwd())
      m = message
      invalid_media_type = "\n**⚠️ 614 Unsupported Media Type:**\n\n Media type not Supported\n\n To see supported media types, send /media_types"
      if not "http" in message.text:
        message.reply("That is not a valid link. Use /help for more info")
        return True
      else: 
        ctype = get_filename(url)
        if ctype:
            if ctype[0] is None:
              err = "`The link you submitted is invalid.`\n\ Kindly check your link and try again for  I am in no mood to tell you the exact reason 😒"
              message.reply(str(err), quote=True)
              logger.warning(str(err))
              return
            required_file_name = ctype[0]
            fnames = ctype[1]
            sent = message.reply("**Checking:** `{}`\n\n if it exist on my server..".format(required_file_name), quote=True, reply_to_message_id=message.message_id)
            time.sleep(2)
            tnews, size = db.sfileid(url)
            if(tnews != 0):
              time.sleep(2)
              message.reply_cached_media(tnews, caption="Powered with ❤️ - @Bfas237Bots")
              
              sent.delete()
            elif(size == 0):
              rd = 1
              sent.delete()
              start = time.time()
              sent = message.reply("**Downloading...**", quote=True, reply_to_message_id=message.message_id)
              time.sleep(3)
              
              downl = DownLoadFile(url, required_file_name, fnames, client, sent, message.chat.id)

              if downl:
                if (downl != 0):
                  sent.edit("Done ✅.. Now uploading..")
                  time.sleep(3)
                  chat_id = message.from_user.id
                  required_file_name = download_path+"/"+required_file_name
                  logger.warning('"%s" Just downloaded:  "%s"', message.from_user.id, required_file_name)
                  mediaq = check_media(required_file_name)
                  file = ""
                  if mediaq == 'Pictures':
                    file = client.send_photo(message.chat.id, required_file_name, progress = DFromUToTelegramProgress, progress_args = (sent, message.chat.id, start, "**📤 Uploading:**"))
                  elif mediaq == 'Video':
                    file = client.send_video(message.chat.id, required_file_name, progress = DFromUToTelegramProgress, progress_args = (sent, message.chat.id, start, "**📤 Uploading:**"))
                  elif mediaq == 'Music':
                    file = client.send_audio(message.chat.id, required_file_name, progress = DFromUToTelegramProgress, progress_args = (sent, message.chat.id, start, "**📤 Uploading:**"))
                  else:
                    file = client.send_document(message.chat.id, required_file_name, progress = DFromUToTelegramProgress, progress_args = (sent, message.chat.id, start, "**📤 Uploading:**"))
                  logs = -1001249303594

                  #client.send_message(chat_id="bfaslogs", text="**Download Logs**\n\n{}".format(log), disable_web_page_preview=True)
                  os.remove(required_file_name)
                  download_id = generate_uuid()
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
                    file_size = file.photo.sizes[-1]["file_size"]
                    file_id = file.photo.sizes[-1]["file_id"]
                    nowq = datetime.now()
                    current_date_time = str(nowq).split(" ")[0] + " " + str(nowq.hour) + ":" + str(nowq.minute) + ":" + str(nowq.second)
                    file_name = fnames +"_"+ current_date_time + ".jpg"
                    extension = get_extension(file)
                  elif file.sticker:
                    if m.chat.type == 'private':
                      m.reply(nauth)
                      return
                  elif file.voice:
                    if m.chat.type == 'private':
                      m.reply(nauth)
                      return
                  elif file.animation:
                    if m.chat.type == 'private':
                      m.reply(nauth)
                      return
                  elif file.videonote:
                    if m.chat.type == 'private':
                      m.reply(nauth)
                      return
                  else:
                    pass
                  uploader = message.from_user.id
                  
                  chk = db.filen(file_name)
                  if(chk == required_file_name):
                    rnd = random_with_N_digits(2)
                    file_name = file.document.file_name+"_"+str(rnd)
                  times = datetime.now().strftime("%I:%M%p")
                  dates = datetime.now().strftime("%B %d, %Y")
                  now = datetime.now()
                  year = int(now.strftime("%Y"))
                  month = int(now.strftime("%m"))
                  day = int(now.strftime("%d"))
                  h = int(now.strftime("%H"))
                  m = int(now.strftime("%M"))
                  s = int(now.strftime("%S"))
                  
                  media = check_media(required_file_name)
                  if not media:
                    message.reply(invalid_media_type)
                    return
                  db.fetchNews(file_name, file_size, file_id, download_id, times, dates, str(uploader), url, year, month, day, h, m, s, 0, media)
                  logger.warning('You just uploaded an:  "%s"', media)
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

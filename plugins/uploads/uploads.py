from utils.typing import *
from utils.menus import *
import traceback
DOWNLOAD_LOCATION = "./DOWNLOADS"


@Client.on_message(Filters.media & Filters.incoming)
def my_handler(bot, m):
    data = list()

    ids = []
    chat_id = m.chat.id
    user = m.from_user.id
    ids.append(user)
    file = m
    file_name = ""
    file_size = ""
    extension = ""
    media = ""
    #print(m)
    download_id = generate_uuid()
    nauth = "\n**⚠️ 541 Unknown Media Type:**\n\n Media type not allowed\n\n To see supported media types, send /media_types"
    invalid_media_type = "\n**⚠️ 614 Unsupported Media Type:**\n\n Media type not Supported\n\n To see supported media types, send /media_types"
    if file.document:
      file_size = file.document.file_size
      file_name = file.document.file_name
      file_id = file.document.file_id
      extension = guess_extension(file.document.mime_type) 
      media = check_media(file_name)
    elif file.video:
      file_size = file.video.file_size
      file_name = file.video.file_name
      file_id = file.video.file_id
      mime = file.video.mime_type
      extension = guess_extension(file.video.mime_type)
      media = "Video"
    elif file.audio:
      file_size = file.audio.file_size
      file_name = file.audio.file_name
      file_id = file.audio.file_id
      extension = guess_extension(file.audio.mime_type)
      media = "Music"
    elif file.photo:
      file_size = file.photo.sizes[-1]["file_size"]
      file_id = file.photo.sizes[-1]["file_id"]
      download_id = generate_uuid()
      file_name = file.photo.id + ".jpg"
      extension = get_extension(file)
      media = "Pictures"
    elif file.voice:
      file_size = file.voice.file_size
      file_name = "voice_"+str(file.voice.date)
      file_id = file.voice.file_id
      extension = guess_extension(file.voice.mime_type)
      media = "Voice"
     
    elif file.video_note:
      if m.chat.type == 'private':
        m.reply(nauth)
    elif file.sticker:
      if m.chat.type == 'private':
        m.reply(nauth)
      return
    elif file.animation:
      if m.chat.type == 'private':
        m.reply(nauth)
      return
    else:
      pass
    if not media:
      m.reply(invalid_media_type)
      return
    logger.warning('You just uploaded an:  "%s"', media)
    admin = ''
    message = m
    try:

      chat_id = message.chat.id
      uploader = user
      url = "https://t.me/jhbjh14514jjhbot"
      if file.photo:
          chk, ext = splitext(file_name)
          logger.info(chk)
          
      chk = doc(file_name)
      item = ""
      private = 0
      if (chk != 0):
        num, row, fid, dat, tim, siz, did = vfileid(chk)
        if row:
            user = ufil(did, str(uploader))
            ids.append(user)
            usr = getuser(did, str(uploader))
            idss = [str(uploader), usr]
            d, df, ff, h, m, s = cdate(did)

            ds = datetime(d, df, ff, h, m, s)

            logger.info(ids)
            if(user != 0):
                item = (
              "🆔 :  #{} \n\n"
              "ℹ️ :  <b>{}</b>\n\n"
              "⌛️ :  <i>{}</i>    |    🕰  <i>{}</i>\n\n"
              "⚖️ <i>{}</i>\n"
              "------------------------------""".format(str(num), str(row[:50]), dat, timedate(ds), pretty_size(int(siz))))

                bot.send_chat_action(chat_id,'TYPING')
                time.sleep(1)
                private = 1
            else:
                item = (
              "🆔 :  #{} \n\n"
              "ℹ️ :  <b>{}</b>\n\n"
              "⌛️ :  <i>{}</i>    |    🕰  <i>{}</i>\n\n"
              "⚖️ <i>{}</i>\n"
              "------------------------------""".format(str(num), str(row[:50]), dat, timedate(ds), pretty_size(int(siz))))


            kb = doc_keyboard(id=did, admin=usr in idss if usr else False, confirmed=user in ids if user else False, ids=user, chat_id=chat_id, private=private, auth=[])
            reply_markup = InlineKeyboardMarkup(kb)


      else:
        download_id = generate_uuid()
        now = datetime.now()
        year = int(now.strftime("%Y"))
        month = int(now.strftime("%m"))
        day = int(now.strftime("%d"))
        h = int(now.strftime("%H"))
        m = int(now.strftime("%M"))
        s = int(now.strftime("%S"))
        times = datetime.now().strftime("%I:%M%p")
        dates = datetime.now().strftime("%B %d, %Y")

        addtoDb(file_name, file_size, file_id, download_id, times, dates, str(uploader), url, year, month, day, h, m, s, 0, media)


        chk = doc(file_name)
        item = ""
        row = "" 
        private = 0
        if (chk != 0):
          num, row, fid, dat, tim, siz, did = vfileid(chk)
        if row:
            user = ufil(did, str(uploader))
            ids.append(user)
            usr = getuser(did, str(uploader))
            idss = [str(uploader), usr]
            d, df, ff, h, m, s = cdate(did)

            ds = datetime(d, df, ff, h, m, s)

            logger.info(ids)
            if(user != 0):
                item = (
              "🆔 :  #{} \n\n"
              "ℹ️ :  <b>{}</b>\n\n"
              "⌛️ :  <i>{}</i>    |    🕰  <i>{}</i>\n\n"
              "⚖️ <i>{}</i>\n"
              "------------------------------""".format(str(num), str(row[:50]), dat, timedate(ds), pretty_size(int(siz))))

                bot.send_chat_action(chat_id,'TYPING')
                time.sleep(1)
                private = 1
            else:
                item = (
              "🆔 :  #{} \n\n"
              "ℹ️ :  <b>{}</b>\n\n"
              "⌛️ :  <i>{}</i>    |    🕰  <i>{}</i>\n\n"
              "⚖️ <i>{}</i>\n"
              "------------------------------""".format(str(num), str(row[:50]), dat, timedate(ds), pretty_size(int(siz))))

                bot.send_chat_action(chat_id,'TYPING')
                time.sleep(1)

            kb = doc_keyboard(id=did, admin=usr in idss if usr else False, confirmed=user in ids if user else False, ids=user, chat_id=chat_id, private=private, auth=[])  
            reply_markup = InlineKeyboardMarkup(kb)
    except sqlite3.ProgrammingError as e:
          logger.debug(e)
          message.reply("Hold on! {}, you are spamming take it easy. 🙄:(".format(message.from_user.first_name))
          return
    except FileIdInvalid as e:
          logger.debug(e)

          message.reply("⚠️ **401 Fatal Error:** \n\nI have notifed my master. He should be fixing it by now")

          return


from utils.typing import *
import utils.menus
import traceback
 
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
          bot.send_chat_action(chat_id,'TYPING')
          time.sleep(1.5)
          m.reply("😔 `404` **Invalid FILE_ID**.\n\n Send /files to see your saved files")

          pass
    else:

        bot.send_chat_action(chat_id,'TYPING')
        time.sleep(1.5)
        m.reply("😔 `404` **Invalid FILE_ID**.\n\n Send /files to see your saved files")




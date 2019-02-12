from utils.typing import *

@Client.on_message(Filters.regex("remove_"))
def my_handler(bot, m):
    chat_id = m.chat.id
    user = m.from_user.id
    h = m.text
    tnews = h[8:] 
    #m.reply(tnews)
    apk_string = "{}".format("apks")
    try:
      if tnews:
        conn = sqlite3.connect('inshorts.db')
        c = conn.cursor()

        chat_id = str(m.from_user.id)

        report = "❗Report\n✔️ File successfully deleted from your storage:\n\n"
        err = "\n❌ Invalid file token:\n\n"

        for s in tnews:
            rc = c.execute("DELETE FROM files WHERE User=? AND DownloadId=?", (chat_id, s,)).rowcount
            if rc <= 0:
                ck = 0
                err += s
            else:
                ck = 1
                report += s

        conn.commit()
        conn.close()
        if (ck == 1):
          m.reply(report)
        else:
          m.reply(err)
    
      else:
        bot.send_chat_action(chat_id,'TYPING')
        time.sleep(1.5)
        m.reply("Syntax error. Press /help for more info")
 
    except Exception as e:
        m.reply(str(e))

       
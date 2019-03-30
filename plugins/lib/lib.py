from utils.typing import *
from utils.broadcast import *
db = DBHelper()
limit = 100

        

@Client.on_message(Filters.command("lib"))
def sendServerStartedMessage(bot, m):
    link = " ".join(m.command[1:])
    chat_id = m.chat.id
    bot.send_chat_action(chat_id,'TYPING')
    # Connecting to the SQL database
    conn = sqlite3.connect('inshorts.db')
    c = conn.cursor()
    con = conn.cursor()
    
    dd = m.from_user.id
    chat_id = str(dd)
    c.execute("SELECT ID, Fname, DownloadId, Size FROM files ORDER BY ID ASC")
    con.execute("SELECT DISTINCT COUNT(*) FROM files")
    user = con.fetchone()
    if user is not None:
       row = user[0]
    else:
        row = None
    rows = c.fetchall() 
    conn.close()
    try:  
      if len(rows) > 0: 
        items = ""
        lens = len(rows)
        username = m.from_user.username
        m.reply("📊 <b>Global Statistics</b>:   \n\n📤 <b>Uploaded Files: {}</b> \n\n👥 <b>Total Users: {}</b>".format(row, db.total()), parse_mode="html")
      else:
        m.reply("No items in your list")
 
    except Exception as e:
        m.reply(str(e))
      
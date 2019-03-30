from utils.typing import *
from utils.broadcast import *
db = DBHelper()
limit = 100
import threading
import time

import threading, time, signal

class Telegram:
    def __init__(self,token,user_id):
        self.both_auth_token = token
        self.user_id = user_id
    
    def sendServerStartedMessage(self):
        token = self.both_auth_token
        user_id = self.user_id


        try:   
            requests.post("https://api.telegram.org/bot" + token + "/sendMessage",data={'chat_id':user_id, 'text': "I was executed successfully "})
            logger.info("hello world")# your code here
            
 
        except Exception as e:
            requests.post("https://api.telegram.org/bot" + token + "/sendMessage",data={'chat_id':user_id, 'text':e})

bot_token = "770345593:AAFMv-pgqjvlaHQYBK71QdoktZDnARYYRuY"
     
user_id = -1001139726492 # put your id here
    
telegram_bot = Telegram(bot_token,user_id)
class ProgramKilled(Exception):
    pass
def signal_handler(signum, frame):
    raise ProgramKilled
    
class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs
        
    def stop(self):
                self.stopped.set()
                self.join()
    def run(self):
            while not self.stopped.wait(self.interval.total_seconds()):
                self.execute(*self.args, **self.kwargs)
            
def d(bot, m, text):
    m.edit("I was executed successfully in {} seconds".format(text))
    logger.info("ended")
    try: job.stop()
    except NameError: pass

WAIT_TIME_SECONDS = 1
 
now = datetime.now()
s1 = now.strftime("%m-%d")  
t1 = datetime(int(now.strftime("%Y")), int(now.strftime("%m")), int(now.strftime("%d")), int(now.strftime("%H")), int(now.strftime("%M")), int(now.strftime("%S")))
t1r = t1 + timedelta(hours=1)  
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)  
LOCAL_TIMEZONE = datetime.now(timezone.utc).astimezone().tzinfo
if LOCAL_TIMEZONE == "UTC":
  t1d = t1r   
else:
  t1d = t1 

  
@Client.on_message(Filters.command("send"))
def send(bot, m, *args, **kwargs):
    don = "don't spam please lol"
    text = " ".join(m.command[1:])
    if (len(text) <= 0):
      sent = m.reply(don)
      return
    
    
      
    user=m.from_user.first_name
    sen = {}
    if m.chat.type == 'private':
       id=m.from_user.id
    else:
      id=m.chat.id
    total_users = db.getusertocontact(limit)
    cc = db.checkifexist(id)
    noc = db.total("notcontacted")
    try: 
      t = int(re.search(r'\d+', text).group())
      timeLeft = int(t) 
      go = m.reply("**I will execute in exactly:** {}".format(timeLeft))
      while timeLeft > 0:
        try:
          logger.info(timeLeft)
          go.edit("**Countdown:** {}".format(timeLeft))
          time.sleep(1)
          timeLeft = timeLeft - 1
        except FloodWait as e:
          m.reply("**FloodWait:** {}".format(e.x))
          time.sleep(e.x)
        except ProgramKilled:
          logger.info("Program killed: running cleanup code")
          job.stop()
          break
      
      job = Job(interval=timedelta(seconds=0), execute=d(bot, go, t)) 
      job.start()
    
    except AttributeError:
      for users in total_users: 
          for user in users:
              try:
                sent = bot.send_message(user, text, parse_mode="html")
                db.updateuser_to_contacted(user)
              except UserIsBlocked:
                us = bot.get_users(user)
                sent = bot.send_message(id, "user [{}](tg://user?id={}) blocked the bot".format(us.first_name, user))
                pass 
        
      else:
        bot.send_message(id, "all messages sent successfully")  
    db.refresh_contacted()     
     
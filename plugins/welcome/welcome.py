from utils.typing import *
from time import time, sleep
import pickle

spamcount = 0
spamlimit = 3
sleeptime = 0
spamtime = 0
spamwait = 10
wait = 0
style_chats = {}
help_message = ''


@Client.on_message(Filters.new_chat_members | Filters.command('show_welcome', '#'))
def welcome(client, message):
    with open('trigger', 'rb') as f:
        welcomes = pickle.load(f)
    if message.chat.id in welcomes:
        if message.command:
            message.reply(welcomes[message.chat.id])
            return
        new_members = ", ".join(
            ["[{}](tg://user?id={})".format(i.first_name, i.id) for i in message.new_chat_members])

        text = welcomes[message.chat.id].replace('%name', new_members)

        # Send the welcome message
        client.send_message(message.chat.id,
                            text,
                            reply_to_message_id=message.message_id,
                            disable_web_page_preview=True)


@Client.on_message(Filters.command('setwelcome', '#'))
def setwelcome(client, message):
    if sleeptime < time():
        with open('trigger', 'rb') as f:
            welcomes = pickle.load(f)
        welcomes[message.chat.id] = message.text.replace('#setwelcome', '')
        with open('trigger', 'wb') as f:
            pickle.dump(welcomes, f)
        message.reply('`Welcome Message succesfully set.`')
        sleep(3)
        client.delete_messages(message.chat.id, message.message_id)

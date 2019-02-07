import requests

from pyrogram import Client, Filters

BASE = "https://hastebin.com"


@Client.on_message(Filters.command("haste", prefix="!") & Filters.reply)
def haste(client, message):
    reply = message.reply_to_message

    if reply.text is None:
        return
 
    #message.delete()

    result = requests.post(
        "{}/documents".format(BASE),
        data=reply.text.encode("UTF-8")
    ).json() 

    message.reply(
        "{}/{}.py".format(BASE, result["key"]),
        reply_to_message_id=reply.message_id
    )
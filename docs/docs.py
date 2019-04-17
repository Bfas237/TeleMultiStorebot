from pyrogram import Emoji
from telegram import InlineQueryResultArticle, InlineQueryResultCachedDocument, InlineQueryResultCachedVideo, InlineQueryResultCachedAudio, InlineQueryResultCachedPhoto, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown
NEXT_OFFSET = 25
CACHE_TIME = 5
DOC_THUMB = "https://i.imgur.com/AggHpo9.png"
SOFTWARE_THUMB = "https://i.imgur.com/6YVH0cr.png"
IMG_THUMB = "https://i.imgur.com/fSSxJkv.png"
APK_THUMB = "https://i.imgur.com/hOcYDWZ.png"
MEDIA_THUMB = "https://i.imgur.com/BduvHoV.png"
GLOBAL_THUMB = "https://i.imgur.com/HQs8dvW.png"
FILES_THUMB = "https://i.imgur.com/zL4AJqh.png"
MP3_THUMB = "https://i.imgur.com/D7ILLy6.png"
HELP_THUMB = "https://i.imgur.com/6jZsMYG.png"

APK_SEARCH_THUMB = "https://i.imgur.com/HYX5seP.png"
MISC_SEARCH_THUMB = "https://i.imgur.com/UVoYOYm.png"
GLOBAL_SEARCH_THUMB = "https://i.imgur.com/8FJuWCr.png"

OTHER_THUMB = "https://i.imgur.com/d1tf976.png"
NOT_FOUND = "https://i.imgur.com/nMQD6QN.png"
ABOUT_BOT_THUMB = "https://i.imgur.com/zRglRz3.png"

INLINE_HELP_SOFTWARE_THUMB = "https://i.imgur.com/lOZy5Db.png"
INLINE_HELP_MOBILE_THUMB = "https://i.imgur.com/gq3baOK.png"

HELP = (
    "{} **TELE MULTISTORE BOT**\n\n"
    "Use this bot inline to search for Uploaded, files, videos, games, apps and other misc files\n\n"

    "**Search**\n"
    "`@jhbjh14514jjhbot <terms>` – Global Search\n"
    "`@jhbjh14514jjhbot !me <terms>` – Privately Search your storage\n"
    "`@jhbjh14514jjhbot !v <terms>` – Search for videos\n\n"

    "**List**\n"
    "`@jhbjh14514jjhbot !me` – Private search\n"
    "`@jhbjh14514jjhbot !p` – Pictures\n"
    "`@jhbjh14514jjhbot !z` – Zip files\n"
    "`@jhbjh14514jjhbot !a` – Apk\n"
    "`@jhbjh14514jjhbot !v` – Videos\n"
    "`@jhbjh14514jjhbot !r` – Rar Files\n"
    "`@jhbjh14514jjhbot !ms` – Misc Files\n\n".format(Emoji.ROBOT_FACE)
)
HELP_INLINE = (
    "{} **TELE MULTISTORE BOT**\n\n"
    "To better understand how it works, lets go inline\n\n".format(Emoji.ROBOT_FACE)
) 

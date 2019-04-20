from pyrogram import Emoji
from telegram import InlineQueryResultArticle, InlineQueryResultCachedDocument, InlineQueryResultCachedVideo, InlineQueryResultCachedAudio, InlineQueryResultCachedVoice,  InlineQueryResultCachedPhoto, ParseMode, \
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
CONTRIBUTE_THUMB = "https://i.ibb.co/cx4yGKr/icon-donate-9875400d4f44e8de9c0b5dbc812ce66c.png"

APK_SEARCH_THUMB = "https://i.imgur.com/HYX5seP.png"
MISC_SEARCH_THUMB = "https://i.imgur.com/UVoYOYm.png"
GLOBAL_SEARCH_THUMB = "https://i.imgur.com/8FJuWCr.png"

OTHER_THUMB = "https://i.imgur.com/d1tf976.png"
NOT_FOUND = "https://i.imgur.com/nMQD6QN.png"
ABOUT_BOT_THUMB = "https://i.imgur.com/zRglRz3.png"

INLINE_HELP_SOFTWARE_THUMB = "https://i.imgur.com/lOZy5Db.png"
INLINE_HELP_MOBILE_THUMB = "https://i.imgur.com/gq3baOK.png"

HELP = (
    "{} *TELE MULTISTORE BOT*\n\n"
    "Use this bot inline to search for Uploaded, files, videos, games, apps and other misc files\n\n"

    "*Search Examples*\n"
    "`@TeleMultiStoreBot <terms>` – Global Search\n"
    "`@TeleMultiStoreBot !soft <terms>` – Privately Search your storage\n"
    "`@TeleMultiStoreBot !store <terms>` – Search apps and games\n\n"

    "*List*\n"
    "`@TeleMultiStoreBot !pic` – Search Pictures\n"
    "`@TeleMultiStoreBot !zip` – Search Archive files\n"
    "`@TeleMultiStoreBot !store` – Search apps and games\n"
    "`@TeleMultiStoreBot !vid` –  Search movies and series\n"
    "`@TeleMultiStoreBot !mp3` – Search songs\n"
    "`@TeleMultiStoreBot !doc` – Search Pdfs, docs, epub\n\n".format(Emoji.ROBOT_FACE)
)
HELP_INLINE = (
    "{} *TELE MULTISTORE BOT*\n\n"
    "To better understand how it works, lets go inline\n\n".format(Emoji.ROBOT_FACE)
) 
CONTRIBUTE = (
    "❤️ *CONTRIBUTIONS*\n\n"
    "🌐 The main purpose of this bot is to make available thousands "
    "of files to millions of telegram users which we take it "
    "as a sole responsibility to do. \n\n"
  
    "🌐 For your own part, all you have to do is forward any file to this bot "
    "and it will be saved and made available for anyone who may search for it \n\n"
  
    "🆘 Feel free to report any bug in our support group for by doing so "
    "You are helping us to help others. \n\n"
    
    "@Bfas237Bots `at your service`"
) 

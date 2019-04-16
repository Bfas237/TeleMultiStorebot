from utils.typing import *
from pyrogram import (
    api, Emoji, Client, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaDocument 
)
data = {'details': {}, 'download':{}} 
state = {}
import logging
logging.getLogger("pyrogram").setLevel(logging.WARNING)
NEXT_OFFSET = 25
CACHE_TIME = 5

FIRE_THUMB = "https://i.imgur.com/9lQUnXj.png"
GLOBAL_THUMB = "https://i.imgur.com/HQs8dvW.png"
APK_THUMB = "https://i.imgur.com/N6iUS0U.png"
OPEN_BOOK_THUMB = "https://i.imgur.com/v1XSJ1D.png"
MEDIA_THUMB = "https://i.imgur.com/BduvHoV.png"
FILES_THUMB = "https://i.imgur.com/zL4AJqh.png"
OTHER_THUMB = "https://i.imgur.com/d1tf976.png"
NOT_FOUND = "https://i.imgur.com/nMQD6QN.png"
ABOUT_BOT_THUMB = "https://i.imgur.com/zRglRz3.png"
SEARCH_THUMB = "https://i.imgur.com/8FJuWCr.png"
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
from base64 import b64decode
from struct import unpack

def parse_inline_message_id(inline_message_id):
    inline_message_id += "=" * ((4 - len(inline_message_id) % 4) % 4) 
    dc_id, _id, access_hash = unpack("<iqq",b64decode(inline_message_id,"-_"))
    return api.types.InputBotInlineMessageID(dc_id=dc_id,id=_id,access_hash=access_hash)


@Client.on_inline_query() 
def answer(client, inline_query):
    query = inline_query.query.lower()
    logger.info(query) 
    chat_id = inline_query.from_user.id
    userd = chat_id 
    articles = []
    sw = []
    conn = sqlite3.connect('inshorts.db') 
    c = conn.cursor()
    con = conn.cursor()
    switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.OPEN_FILE_FOLDER)
    DEFAULT_RESULTS = [
            InlineQueryResultArticle(
                id=uuid4(),
                title="About Tele MultiStore Bot",
                input_message_content=InputTextMessageContent(
            "{} **Tele MultiStore**\n\n"
            "Tele MultiStore is an advanced, easy-to-use Telegram bot that replaces keeps track of all "
            "your uploaded files either through forwading, uploading "
            "or downloading from the web.".format(Emoji.CARD_INDEX_DIVIDERS),
                ),
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton('Click me!',callback_data=b'inline_click')]]
                ),
                description="How to use Tele MultiStore",
                thumb_url=ABOUT_BOT_THUMB 
            ),
            InlineQueryResultArticle(
                id=uuid4(),
                title="Usage",
                input_message_content=InputTextMessageContent(HELP),
                description="How to use Tele MultiStore Bot",
                thumb_url=FILES_THUMB
            )
            
        ]
    string = inline_query.query.lower()
    
    if string == "":
        inline_query.answer(
            results=DEFAULT_RESULTS,
            cache_time=CACHE_TIME, 
            is_personal=True,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
        )

        return
    offset = int(inline_query.offset or 0)
    
    if query.startswith('!f'):
      likeDate = "%" + str(query[3:]) + "%"
      logger.warning(likeDate) 
      c.execute('SELECT DownloadId, Fname, FileId FROM files WHERE Fname LIKE ? OR DownloadId LIKE ? ORDER BY ID DESC LIMIT 8 OFFSET ?', (likeDate, likeDate, offset ))
      result = c.fetchall() 
      con.execute("SELECT DISTINCT COUNT (*) FROM files WHERE User = ?", (chat_id, ))  
    
      rowcount = con.fetchone()[0]
      things = [list(i) for i in result]
      logger.warning('Query "%s"', things)  
      if offset == 0:
            articles.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="Media",
                    description="Your can search for any media",
                    input_message_content=InputTextMessageContent(
                        "🖼 **Media Finder**\n\n"
                        "`This section deals with all medias in your storage`"
                    ),
                    thumb_url=FIRE_THUMB,
                )
            )
      switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.BALLOT_BOX_WITH_BALLOT)
      if things:
        s = 's'
        all = 'Media'
        
        for num, th in enumerate(things):
          sw.append(str(th[0]))
          articles.append(InlineQueryResultArticle(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=MEDIA_THUMB,
                    description="Click to view the details",
                    input_message_content=InputTextMessageContent(
                    "{}".format(str(th[1]))
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🔄 Send to another Chat", switch_inline_query="!f "+str(sw[0]))], [InlineKeyboardButton("📥 Instant Download", url="https://telegram.me/jhbjh14514jjhbot?start=dl_"+str(sw[0]))]
                    ]  
                ))) 
        count = len(articles) - 1
        
        switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.OPEN_BOOK, count, s if count > 1 else '', all if string == "!f" else str(query[3:]))
      elif not things:  
        s = 's'
        all = 'Media'
        articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Your search returned Nothing", thumb_url=NOT_FOUND,
                    description="Try Searching for ("+str(rowcount)+")",
                    input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ))] 
        count = len(articles) - 1
        
        switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.OPEN_BOOK, count, s if count > 1 else '', all if string == "!f" else str(query[3:]))
      
      count = len(articles) - 1
      if articles:
        inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            next_offset=offset,
        ) 
    else:
        if offset:
            inline_query.answer(
                results=[],
                cache_time=CACHE_TIME,
                switch_pm_text=switch_pm_text,
                switch_pm_parameter="start",
                next_offset="",
            )
            
        string = " ".join(string)
        logger.warning(string)
        if string == "":
          inline_query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text="{} Type to search Raw Docs".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
                    switch_pm_parameter="start",
                )
          
        elif len(string) > 0:
          articles.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="Global Search",
                    description="Search globally for any uploaded file or media",
                    input_message_content=InputTextMessageContent(
                        "{} **Global Search**\n\n"
                        "`You can search globally for any uploaded file, media that has been uploaded to my storage. It doesn't matter if you are the uploader`".format(Emoji.MAGNIFYING_GLASS_TILTED_LEFT)
                    ),
                    thumb_url=SEARCH_THUMB,
                )
            )
          likeDate = "%" + str(query) + "%"
           
          c.execute('SELECT DownloadId, Fname, FileId FROM files WHERE Fname LIKE ? OR DownloadId LIKE ? ORDER BY ID DESC LIMIT 8 OFFSET ?', (likeDate, likeDate, offset ))
          result = c.fetchall() 
          con.execute("SELECT DISTINCT COUNT (*) FROM files WHERE User = ?", (chat_id, ))  
    
          rowcount = con.fetchone()[0]
          things = [list(i) for i in result]
          if things:
            s = 's'
            all = 'Media'
            for num, th in enumerate(things):
              sw.append(str(th[0]))
              articles.append(InlineQueryResultArticle(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=GLOBAL_THUMB,
                    description="Click to view the details",
                    input_message_content=InputTextMessageContent(
                    "{}".format(str(th[1]))
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🔄 Send to another Chat", switch_inline_query="!f "+str(sw[0]))], [InlineKeyboardButton("📥 Instant Download", url="https://telegram.me/jhbjh14514jjhbot?start=dl_"+str(sw[0]))]
                    ]  
                ))) 
                
            count = len(articles) - 1
        
                
            switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.OPEN_BOOK, count, s if count > 1 else '', all if string == "!f" else str(query))
          elif not things:  
            s = 's'
            all = 'Media'
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Your search returned Nothing", thumb_url=NOT_FOUND,
                    description="Click to view details",
                    input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ))] 
            count = len(articles) * 0
            strings = (string[:8] + '..') if len(string) > 10 else string
            switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.CROSS_MARK, str(count), s if count > 1 else '', strings if count <= 1 else str(query))
        if articles:
          inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            next_offset=offset,
        ) 
        else:
            inline_query.answer(
                results=[],
                cache_time=CACHE_TIME,
                switch_pm_text='{} No results for "{}"'.format(Emoji.CROSS_MARK, string),
                switch_pm_parameter="okay",
            )

      #inline_query.answer(articles, cache_time=1, is_personal=True)


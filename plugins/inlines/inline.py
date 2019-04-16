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
                description="How to use Tele MultiStore",
                thumb_url=ABOUT_BOT_THUMB 
            ),
            InlineQueryResultArticle(
                id=uuid4(),
                title="Usage",
                input_message_content=InputTextMessageContent(HELP),
                description="How to use Tele MultiStore Bot",
                thumb_url=FILES_THUMB
            ),
            InlineQueryResultArticle(
                id=uuid4(),
                title="Help and Faqs",
                input_message_content=InputTextMessageContent(HELP_INLINE),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("⏏️ Inline Help 🆘", switch_inline_query_current_chat="!h")]
                    ]  
                ),
                description="Useful faqs on how it works",
                thumb_url=HELP_THUMB
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
    su = []
    if query.startswith('!pic'):
      likeDate = "%" + str(query[5:]) + "%"
      media = "Pictures"
      logger.warning(likeDate) 
      c.execute('SELECT DownloadId, Fname, FileId, Media FROM files WHERE Media = ? AND Fname LIKE ? ORDER BY ID DESC LIMIT 8 OFFSET ?', (media, likeDate, offset ))
      result = c.fetchall() 
      con.execute("SELECT DISTINCT COUNT (*) FROM files WHERE Media = ?", (media, ))  
      rowcount = con.fetchone()[0]
      things = [list(i) for i in result]
      logger.warning('Query "%s"', things) 
      for ft in things:
        su.append(str(ft[3]))
      if offset == 0:
            articles.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=str(su[0]),
                    description="Your can search for any media",
                    input_message_content=InputTextMessageContent(
                        "🖼 **Media Finder**\n\n"
                        "`This section deals with all medias in your storage`"
                    ),
                    thumb_url=MISC_SEARCH_THUMB,
                )
            )
      switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.BALLOT_BOX_WITH_BALLOT)
      if things:
        s = 's'
        all = str(su[0])
        
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
        res = ""
        ress = ""
        if len(str(string[5:])) == 0:
          res = "Items in category" if count > 1 else "Item in category"
        if len(str(string[5:])) >= 1:
          ress = "Results for" if count > 1 else "Result for"
        
        switch_pm_text = "{} Found {} {} \"{}\"".format(Emoji.OPEN_BOOK, count, res if len(str(string[5:])) == 0 else ress, all if len(str(string[5:])) < 1 else str(string[5:]))
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
        
        switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.OPEN_BOOK, count, s if count > 1 else '', all if string == "!f" else str(query[5:]))
      
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
        elif query.startswith('!ms'): 
          logger.warning(string)
          if string == "":
            inline_query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text="{} Type to search Raw Docs".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
                    switch_pm_parameter="start",
                )
          
      
          likeDate = "%" + str(string[3:]) + "%"
          media = "Misc"
          logger.warning(likeDate) 
          c.execute('SELECT DownloadId, Fname, FileId, Media FROM files WHERE Media = ? AND Fname LIKE ? ORDER BY ID DESC LIMIT 8 OFFSET ?', (media, likeDate, offset ))
          result = c.fetchall() 
          con.execute("SELECT DISTINCT COUNT (*) FROM files WHERE Media = ?", (media, ))  
          rowcount = con.fetchone()[0]
          things = [list(i) for i in result]
          logger.warning('Query "%s"', things)
          try:
            for ft in things:
              su.append(str(ft[3]))
            if offset == 0:
              articles.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=str(su[0]),
                    description="Your onestop mobile app search",
                    input_message_content=InputTextMessageContent(
                        "🖼 **Mobile Apps finder**\n\n"
                        "`This section deals with all mobile apps. You just need to pass a search term and get the available results`"
                    ),
                    thumb_url=APK_SEARCH_THUMB,
                )
            )
            
          except IndexError as e:
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Nothing has been uploaded so far", thumb_url=NOT_FOUND,
                    description="Try by uploading something first",
                    input_message_content=InputTextMessageContent(
                    "Try uploading something first"
                ))] 
            inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            next_offset=offset,
        ) 
            return
      
          switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.BALLOT_BOX_WITH_BALLOT)
          if things:
            s = 's'
            all = str(su[0])
        
            for num, th in enumerate(things):
              sw.append(str(th[0]))
              articles.append(InlineQueryResultArticle(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=IMG_THUMB,
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
            res = ""
            ress = ""
            if len(str(string[3:])) == 0:
              res = "Items in category" if count > 1 else "Item in category"
            if len(str(string[3:])) >= 1:
              ress = "Results for" if count > 1 else "Result for"
        
            switch_pm_text = "{} Found {} {} \"{}\"".format(Emoji.OPEN_BOOK, count, res if len(str(string[3:])) == 0 else ress, all if len(str(string[3:])) < 1 else str(query[3:]))
          elif not things:  
            s = 's'
            all = 'Misc'
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Your search returned Nothing", thumb_url=NOT_FOUND,
                    description="Try Searching for ("+str(rowcount)+")",
                    input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ))] 
            count = len(articles) - 1
            strings = (string[:8] + '..') if len(string) > 10 else string
            switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.OPEN_BOOK, count, s if count > 1 else '', all if strings == "!f" else str(query[3:]))
      
          count = len(articles) - 1
        
        
        
            
        elif query.startswith('!h'): 
          logger.warning(string)
          INLINE_HELP = [
            InlineQueryResultArticle(
                id=uuid4(),
                title="💻 Software Search",
                input_message_content=InputTextMessageContent(
            "🖥️ **Software Search**\n\n"
            "`Don't hassle any longer for you have it all. Search for your desired software "
            "by typing either the full or just part of the name "
            "or by extension. It works like magic.`\n"
            "\n"
            "**Supported Syntax:**  `@jhbjh14514jjhbot <cmd> <terms>`"
            "\n\n"
            "**Example:**    `@jhbjh14514jjhbot !exe idm`",
                ),
        reply_markup=InlineKeyboardMarkup([[
           
            InlineKeyboardButton(
                "Give it a try",
                switch_inline_query_current_chat="!exe idm"
            )]]),
                description="Learn how to search for software",
                thumb_url=INLINE_HELP_SOFTWARE_THUMB 
            ),
            
            InlineQueryResultArticle(
                id=uuid4(),
                title="📱 Mobile Apps Search",
                input_message_content=InputTextMessageContent(
            "📱 **Mobile Apps Search**\n\n"
            "`You can perform instantaneous app search using any "
            " regex pattern either using the full app name "
            "or by extension. It works like magic.`\n"
            "\n"
            "**Supported Syntax:**  `@jhbjh14514jjhbot <cmd> <terms>`"
            "\n\n"
            "**Example:**    `@jhbjh14514jjhbot !apk telegram`",
                ),
        reply_markup=InlineKeyboardMarkup([[
           
            InlineKeyboardButton(
                "Give it a try",
                switch_inline_query_current_chat="!apk telegram"
            )]]),
                description="Learn how to search for software",
                thumb_url=INLINE_HELP_MOBILE_THUMB 
            )
            
            
        ]
          switch_pm_text = "🆘 TELE MULTISTORE HELP"
          if string == "":
            inline_query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text="{} Type to search Raw Docs".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
                    switch_pm_parameter="start",
                )
          
      
          things = ["ok"]
          logger.warning('Query "%s"', things)
          try:
            for ft in things:
              su.append(str(ft[3]))
          except IndexError as e:
            articles = INLINE_HELP
            inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            next_offset=offset,
        ) 
            return
      
        
        
        elif query.startswith('!apk'): 
          logger.warning(string)
          if string == "":
            inline_query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text="{} Type to search Raw Docs".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
                    switch_pm_parameter="start",
                )
          
      
          likeDate = "%" + str(string[5:]) + "%"
          media = "Apps"
          logger.warning(likeDate) 
          c.execute('SELECT DownloadId, Fname, FileId, Media FROM files WHERE Media = ? AND Fname LIKE ? ORDER BY ID DESC LIMIT 8 OFFSET ?', (media, likeDate, offset ))
          result = c.fetchall() 
          con.execute("SELECT DISTINCT COUNT (*) FROM files WHERE Media = ?", (media, ))  
          rowcount = con.fetchone()[0]
          things = [list(i) for i in result]
          logger.warning('Query "%s"', things)
          try:
            for ft in things:
              su.append(str(ft[3]))
            if offset == 0:
              articles.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=str(su[0]),
                    description="Your onestop mobile app search",
                    input_message_content=InputTextMessageContent(
                        "📱 **Mobile Apps finder**\n\n"
                        "`This section deals with all mobile apps. You just need to pass a search term and get the available results`"
                    ),
                    thumb_url=APK_SEARCH_THUMB,
                )
            )
            
          except IndexError as e:
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Nothing has been uploaded so far", thumb_url=NOT_FOUND,
                    description="Try by uploading something first",
                    input_message_content=InputTextMessageContent(
                    "Try uploading something first"
                ))] 
            inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            next_offset=offset,
        ) 
            return
      
          switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.BALLOT_BOX_WITH_BALLOT)
          if things:
            s = 's'
            all = str(su[0])
        
            for num, th in enumerate(things):
              sw.append(str(th[0]))
              articles.append(InlineQueryResultArticle(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=APK_THUMB,
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
            res = ""
            ress = ""
            if len(str(string[5:])) == 0:
              res = "Items in category" if count > 1 else "Item in category"
            if len(str(string[5:])) >= 1:
              ress = "Results for" if count > 1 else "Result for"
        
            switch_pm_text = "{} Found {} {} \"{}\"".format(Emoji.OPEN_BOOK, count, res if len(str(string[5:])) == 0 else ress, all if len(str(string[5:])) < 1 else str(query[5:]))
          elif not things:  
            s = 's'
            all = 'Apps'
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Your search returned Nothing", thumb_url=NOT_FOUND,
                    description="Try Searching for ("+str(rowcount)+")",
                    input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ))] 
            count = len(articles) - 1
            strings = (string[:8] + '..') if len(string) > 10 else string
            switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.OPEN_BOOK, count, s if count > 1 else '', all if strings == "!f" else str(query[5:]))
      
          count = len(articles) - 1
        
        
        elif query.startswith('!exe'): 
          logger.warning(string)
          if string == "":
            inline_query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text="{} Type to search Raw Docs".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
                    switch_pm_parameter="start",
                )
          
      
          likeDate = "%" + str(string[5:]) + "%"
          media = "Software"
          logger.warning(likeDate) 
          c.execute('SELECT DownloadId, Fname, FileId, Media FROM files WHERE Media = ? AND Fname LIKE ? ORDER BY ID DESC LIMIT 8 OFFSET ?', (media, likeDate, offset ))
          result = c.fetchall() 
          con.execute("SELECT DISTINCT COUNT (*) FROM files WHERE Media = ?", (media, ))  
          rowcount = con.fetchone()[0]
          things = [list(i) for i in result]
          logger.warning('Query "%s"', things)
          try:
            for ft in things:
              su.append(str(ft[3]))
            if offset == 0:
              articles.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=str(su[0]),
                    description="Your onestop mobile app search",
                    input_message_content=InputTextMessageContent(
                        "🖼 **Mobile Apps finder**\n\n"
                        "`This section deals with all mobile apps. You just need to pass a search term and get the available results`"
                    ),
                    thumb_url=APK_SEARCH_THUMB,
                )
            )
            
          except IndexError as e:
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Nothing has been uploaded so far", thumb_url=NOT_FOUND,
                    description="Try by uploading something first",
                    input_message_content=InputTextMessageContent(
                    "Try uploading something first"
                ))] 
            inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            next_offset=offset,
        ) 
            return
      
          switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.BALLOT_BOX_WITH_BALLOT)
          if things:
            s = 's'
            all = str(su[0])
        
            for num, th in enumerate(things):
              sw.append(str(th[0]))
              articles.append(InlineQueryResultArticle(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=SOFTWARE_THUMB,
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
            res = ""
            ress = ""
            if len(str(string[5:])) == 0:
              res = "Items in category" if count > 1 else "Item in category"
            if len(str(string[5:])) >= 1:
              ress = "Results for" if count > 1 else "Result for"
        
            switch_pm_text = "{} Found {} {} \"{}\"".format(Emoji.OPEN_BOOK, count, res if len(str(string[5:])) == 0 else ress, all if len(str(string[5:])) < 1 else str(query[5:]))
          elif not things:  
            s = 's'
            all = 'Software'
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Your search returned Nothing", thumb_url=NOT_FOUND,
                    description="Try Searching for ("+str(rowcount)+")",
                    input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ))] 
            count = len(articles) - 1
            strings = (string[:8] + '..') if len(string) > 10 else string
            switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.OPEN_BOOK, count, s if count > 1 else '', all if strings == "!f" else str(query[5:]))
      
          count = len(articles) - 1
        
        
        
        
        elif query.startswith('!doc'): 
          logger.warning(string)
          if string == "":
            inline_query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text="{} Type to search Raw Docs".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
                    switch_pm_parameter="start",
                )
          
      
          likeDate = "%" + str(string[5:]) + "%"
          media = "Document"
          logger.warning(likeDate) 
          c.execute('SELECT DownloadId, Fname, FileId, Media FROM files WHERE Media = ? AND Fname LIKE ? ORDER BY ID DESC LIMIT 8 OFFSET ?', (media, likeDate, offset ))
          result = c.fetchall() 
          con.execute("SELECT DISTINCT COUNT (*) FROM files WHERE Media = ?", (media, ))  
          rowcount = con.fetchone()[0]
          things = [list(i) for i in result]
          logger.warning('Query "%s"', things) 
          for ft in things:
            su.append(str(ft[3]))
          if (len(str(su)) == 0):
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Your search returned Nothing", thumb_url=NOT_FOUND,
                    description="Try Searching for ("+str(rowcount)+")",
                    input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ))] 
            return
          if offset == 0:
            articles.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=str(su[0]),
                    description="Your onestop mobile app search",
                    input_message_content=InputTextMessageContent(
                        "🖼 **Mobile Apps finder**\n\n"
                        "`This section deals with all mobile apps. You just need to pass a search term and get the available results`"
                    ),
                    thumb_url=APK_SEARCH_THUMB,
                )
            )
      
          switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.BALLOT_BOX_WITH_BALLOT)
          if things:
            s = 's'
            all = str(su[0])
        
            for num, th in enumerate(things):
              sw.append(str(th[0]))
              articles.append(InlineQueryResultArticle(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=DOC_THUMB,
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
            res = ""
            ress = ""
            if len(str(string[5:])) == 0:
              res = "Items in category" if count > 1 else "Item in category"
            if len(str(string[5:])) >= 1:
              ress = "Results for" if count > 1 else "Result for"
        
            switch_pm_text = "{} Found {} {} \"{}\"".format(Emoji.OPEN_BOOK, count, res if len(str(string[5:])) == 0 else ress, all if len(str(string[5:])) < 1 else str(query[5:]))
          elif not things:  
            s = 's'
            all = 'Document'
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Your search returned Nothing", thumb_url=NOT_FOUND,
                    description="Try Searching for ("+str(rowcount)+")",
                    input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ))] 
            count = len(articles) - 1
            strings = (string[:8] + '..') if len(string) > 10 else string
            switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.OPEN_BOOK, count, s if count > 1 else '', all if strings == "!f" else str(query[5:]))
      
          count = len(articles) - 1
        
        
        
        elif query.startswith('!mp3'): 
          logger.warning(string)
          if string == "":
            inline_query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text="{} Type to search Raw Docs".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
                    switch_pm_parameter="start",
                )
          
      
          likeDate = "%" + str(string[5:]) + "%"
          media = "Music"
          logger.warning(likeDate) 
          c.execute('SELECT DownloadId, Fname, FileId, Media FROM files WHERE Media = ? AND Fname LIKE ? ORDER BY ID DESC LIMIT 8 OFFSET ?', (media, likeDate, offset ))
          result = c.fetchall() 
          con.execute("SELECT DISTINCT COUNT (*) FROM files WHERE Media = ?", (media, ))  
          rowcount = con.fetchone()[0]
          things = [list(i) for i in result]
          logger.warning('Query "%s"', things) 
          try:
            for ft in things:
              su.append(str(ft[3]))
            if offset == 0:
              articles.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=str(su[0]),
                    description="Your onestop mobile app search",
                    input_message_content=InputTextMessageContent(
                        "🖼 **Mobile Apps finder**\n\n"
                        "`This section deals with all mobile apps. You just need to pass a search term and get the available results`"
                    ),
                    thumb_url=APK_SEARCH_THUMB,
                )
            )
            
          except IndexError as e:
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Nothing has been uploaded so far", thumb_url=NOT_FOUND,
                    description="Try by uploading something first",
                    input_message_content=InputTextMessageContent(
                    "Try uploading something first"
                ))] 
            inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            next_offset=offset,
        ) 
            return
          switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.BALLOT_BOX_WITH_BALLOT)
          if things:
            s = 's'
            all = str(su[0])
        
            for num, th in enumerate(things):
              sw.append(str(th[0]))
              articles.append(InlineQueryResultArticle(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=MP3_THUMB,
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
            res = ""
            ress = ""
            if len(str(string[5:])) == 0:
              res = "Items in category" if count > 1 else "Item in category"
            if len(str(string[5:])) >= 1:
              ress = "Results for" if count > 1 else "Result for"
        
            switch_pm_text = "{} Found {} {} \"{}\"".format(Emoji.OPEN_BOOK, count, res if len(str(string[5:])) == 0 else ress, all if len(str(string[5:])) < 1 else str(query[5:]))
          elif not things:  
            s = 's'
            all = 'Music'
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Your search returned Nothing", thumb_url=NOT_FOUND,
                    description="Try Searching for ("+str(rowcount)+")",
                    input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ))] 
            count = len(articles) - 1
            strings = (string[:8] + '..') if len(string) > 10 else string
            switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.OPEN_BOOK, count, s if count > 1 else '', all if strings == "!f" else str(query[5:]))
      
          count = len(articles) - 1
        
        
        
        elif query.startswith('!vid'): 
          logger.warning(string)
          if string == "":
            inline_query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text="{} Type to search Raw Docs".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
                    switch_pm_parameter="start",
                )
          
      
          likeDate = "%" + str(string[5:]) + "%"
          media = "Videos"
          logger.warning(likeDate) 
          c.execute('SELECT DownloadId, Fname, FileId, Media FROM files WHERE Media = ? AND Fname LIKE ? ORDER BY ID DESC LIMIT 8 OFFSET ?', (media, likeDate, offset ))
          result = c.fetchall() 
          con.execute("SELECT DISTINCT COUNT (*) FROM files WHERE Media = ?", (media, ))  
          rowcount = con.fetchone()[0]
          things = [list(i) for i in result]
          logger.warning('Query "%s"', things)
          try:
            for ft in things:
              su.append(str(ft[3]))
            if offset == 0:
              articles.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=str(su[0]),
                    description="Your onestop mobile app search",
                    input_message_content=InputTextMessageContent(
                        "🖼 **Mobile Apps finder**\n\n"
                        "`This section deals with all mobile apps. You just need to pass a search term and get the available results`"
                    ),
                    thumb_url=APK_SEARCH_THUMB,
                )
            )
            
          except IndexError as e:
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Nothing has been uploaded so far", thumb_url=NOT_FOUND,
                    description="Try by uploading something first",
                    input_message_content=InputTextMessageContent(
                    "Try uploading something first"
                ))] 
            inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            next_offset=offset,
        ) 
            return
      
          switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.BALLOT_BOX_WITH_BALLOT)
          if things:
            s = 's'
            all = str(su[0])
        
            for num, th in enumerate(things):
              sw.append(str(th[0]))
              articles.append(InlineQueryResultArticle(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=IMG_THUMB,
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
            res = ""
            ress = ""
            if len(str(string[5:])) == 0:
              res = "Items in category" if count > 1 else "Item in category"
            if len(str(string[5:])) >= 1:
              ress = "Results for" if count > 1 else "Result for"
        
            switch_pm_text = "{} Found {} {} \"{}\"".format(Emoji.OPEN_BOOK, count, res if len(str(string[5:])) == 0 else ress, all if len(str(string[5:])) < 1 else str(query[5:]))
          elif not things:  
            s = 's'
            all = 'Videos'
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Your search returned Nothing", thumb_url=NOT_FOUND,
                    description="Try Searching for ("+str(rowcount)+")",
                    input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ))] 
            count = len(articles) - 1
            strings = (string[:8] + '..') if len(string) > 10 else string
            switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.OPEN_BOOK, count, s if count > 1 else '', all if strings == "!f" else str(query[5:]))
      
          count = len(articles) - 1
        
        
        
        elif query.startswith('!zip'): 
          logger.warning(string)
          if string == "":
            inline_query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text="{} Type to search Raw Docs".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
                    switch_pm_parameter="start",
                )
          
      
          likeDate = "%" + str(string[5:]) + "%"
          media = "Archives"
          logger.warning(likeDate) 
          c.execute('SELECT DownloadId, Fname, FileId, Media FROM files WHERE Media = ? AND Fname LIKE ? ORDER BY ID DESC LIMIT 8 OFFSET ?', (media, likeDate, offset ))
          result = c.fetchall() 
          con.execute("SELECT DISTINCT COUNT (*) FROM files WHERE Media = ?", (media, ))  
          rowcount = con.fetchone()[0]
          things = [list(i) for i in result]
          logger.warning('Query "%s"', things)
          try:
            for ft in things:
              su.append(str(ft[3]))
            if offset == 0:
              articles.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=str(su[0]),
                    description="Your onestop mobile app search",
                    input_message_content=InputTextMessageContent(
                        "🖼 **Mobile Apps finder**\n\n"
                        "`This section deals with all mobile apps. You just need to pass a search term and get the available results`"
                    ),
                    thumb_url=APK_SEARCH_THUMB,
                )
            )
            
          except IndexError as e:
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Nothing has been uploaded so far", thumb_url=NOT_FOUND,
                    description="Try by uploading something first",
                    input_message_content=InputTextMessageContent(
                    "Try uploading something first"
                ))] 
            inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            next_offset=offset,
        ) 
            return
      
          switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.BALLOT_BOX_WITH_BALLOT)
          if things:
            s = 's'
            all = str(su[0])
        
            for num, th in enumerate(things):
              sw.append(str(th[0]))
              articles.append(InlineQueryResultArticle(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=IMG_THUMB,
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
            res = ""
            ress = ""
            if len(str(string[5:])) == 0:
              res = "Items in category" if count > 1 else "Item in category"
            if len(str(string[5:])) >= 1:
              ress = "Results for" if count > 1 else "Result for"
        
            switch_pm_text = "{} Found {} {} \"{}\"".format(Emoji.OPEN_BOOK, count, res if len(str(string[5:])) == 0 else ress, all if len(str(string[5:])) < 1 else str(query[5:]))
          elif not things:  
            s = 's'
            all = 'Achives'
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Your search returned Nothing", thumb_url=NOT_FOUND,
                    description="Try Searching for ("+str(rowcount)+")",
                    input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ))] 
            count = len(articles) - 1
            strings = (string[:8] + '..') if len(string) > 10 else string
            switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.OPEN_BOOK, count, s if count > 1 else '', all if strings == "!f" else str(query[5:]))
      
          count = len(articles) - 1
        
        
        
            
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
                    thumb_url=GLOBAL_SEARCH_THUMB,
                )
            )
          likeDate = "%" + str(query) + "%"
           
          c.execute('SELECT DownloadId, Fname, FileId, Media FROM files WHERE Fname LIKE ? OR DownloadId LIKE ? OR Media LIKE ? ORDER BY ID DESC LIMIT 8 OFFSET ?', (likeDate, likeDate, likeDate, offset ))
          result = c.fetchall() 
          con.execute("SELECT DISTINCT COUNT (*) FROM files WHERE User = ?", (chat_id, ))  
          
          rowcount = con.fetchone()[0]
          things = [list(i) for i in result]
          for ft in things:
            su.append(str(ft[3]))
          if things:
            s = 's'
            all = str(su[0])
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
            res = ""
            ress = ""
            nu = ""
            if len(str(string[3:])) == 0:
              res = "Items in category" if count > 1 else "Item in category"
            if len(str(string[3:])) >= 1:
              ress = "Results for" if count > 1 else "Result for"
            if len(str(string[3:])) == 0:
              nu = "and "+str(len(all))+" Others" if count > 1 else ""
            switch_pm_text = "{} Found {} {} \"{} {}\"".format(Emoji.OPEN_BOOK, count, res if len(str(string[3:])) == 0 else ress, all if len(str(string[3:])) < 1 else str(query[3:]), nu)
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
            switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.CROSS_MARK, str(count), s if count > 1 else '', strings if count <= 1 else str(string))
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


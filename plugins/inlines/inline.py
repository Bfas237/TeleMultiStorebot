from utils.typing import *
from docs.docs import *
from telegram.utils.helpers import escape_markdown
import logging
logging.getLogger("pyrogram").setLevel(logging.WARNING)


 
def answer_inline(update, inline_query):
    """Handle the inline query."""
    query = update.inline_query.query
    logger.warning(update) 
    chat_id = update.effective_user.id
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
            "{} *Tele MultiStore*\n\n"
            "Tele MultiStore is an advanced, easy-to-use Telegram bot that replaces keeps track of all "
            "your uploaded files either through forwading, uploading "
            "or downloading from the web.".format(Emoji.CARD_INDEX_DIVIDERS),
                parse_mode=ParseMode.MARKDOWN,
                ),
                description="Tele MultiStore is an advanced storage bot for storing and retriving files",
                thumb_url=ABOUT_BOT_THUMB 
            ),
            InlineQueryResultArticle(
                id=uuid4(),
                title="Usage",
                input_message_content=InputTextMessageContent(HELP,
                parse_mode=ParseMode.MARKDOWN),
                description="Learn some useful commands, tricks, and lots more how to use this bot",
                thumb_url=FILES_THUMB
            ),
            InlineQueryResultArticle(
                id=uuid4(),
                title="Help and Faqs",
                input_message_content=InputTextMessageContent(HELP_INLINE,
                parse_mode=ParseMode.MARKDOWN),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Inline Help 🆘", switch_inline_query_current_chat="!h")]
                    ]  
                ),
                description="Frequently asked questions and other helpful resources",
                thumb_url=HELP_THUMB
            ),
            InlineQueryResultArticle(
                id=uuid4(),
                title="Contribution",
                input_message_content=InputTextMessageContent(CONTRIBUTE,
                parse_mode=ParseMode.MARKDOWN),
                description="How to contribute and make this bot better than it is",
                thumb_url=CONTRIBUTE_THUMB
            )
            
        ]
            
    string = update.inline_query.query.lower()
    
    if string == "":
        update.inline_query.answer(
            results=DEFAULT_RESULTS,
            cache_time=CACHE_TIME, 
            is_personal=True,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
        )

        return
    offset = int(update.inline_query.offset or 0)
    su = []
    if query.startswith('!pic'):
      likeDate = "%" + str(query[5:]) + "%"
      media = "Pictures"
      logger.warning(likeDate) 
      c.execute('SELECT DISTINCT DownloadId, Fname, FileId, Media FROM files WHERE Media = ? AND Fname LIKE ? ORDER BY ID DESC LIMIT 8 OFFSET ?', (media, likeDate, offset ))
      result = c.fetchall() 
      con.execute("SELECT DISTINCT COUNT (*) FROM files WHERE Media = ?", (media, ))  
      rowcount = con.fetchone()[0]
      things = [list(i) for i in result]
      logger.warning('Query "%s"', things) 
      try:
        for ft in things:
          su.append(str(ft[3]))
        if offset == 0:
            articles = [
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=str(su[0]),
                    description="All your desired image in one click",
                    input_message_content=InputTextMessageContent(
                        "🖼 **Image Store**\n\n"
                        "`You can search for all images either by extention or file name if you know`"
                    ),
                    thumb_url=MISC_SEARCH_THUMB,
                )
            ]
      except IndexError as e:
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Nothing has been uploaded so far", thumb_url=NOT_FOUND,
                    description="Try by uploading something first",
                    input_message_content=InputTextMessageContent(
                    "This section happens to be empty.... Sorry!!!"
                ))] 
            update.inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            offset=offset,
        ) 
            return
      switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.BALLOT_BOX_WITH_BALLOT)
      if things:
        s = 's'
        all = str(su[0])
        
        for num, th in enumerate(things):
          sw.append(str(th[0]))
          articles.append(InlineQueryResultCachedPhoto(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=MEDIA_THUMB,photo_file_id="{}".format(str(th[2])),
                    description="Click to view the details",
                    caption="{}".format(str(th[1])),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🔄 Send to another Chat", switch_inline_query=str(sw[0]))]
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
        update.inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            next_offset="" if count <= 49 else offset
        ) 
    else:
        if offset:
            update.inline_query.answer(
                results=[],
                cache_time=CACHE_TIME,
                switch_pm_text=switch_pm_text,
                switch_pm_parameter="start",
                next_offset="",
            )
        
            
        elif query.startswith('!h'): 
          logger.warning(string)
          INLINE_HELP = [
            InlineQueryResultArticle(
                id=uuid4(),
                title="💻 Software Search",
                input_message_content=InputTextMessageContent(
            "🖥️ *Software Search*\n\n"
            "`Don't hassle any longer for you have it all. Search for your desired software "
            "by typing either the full or just part of the name "
            "or by extension. It works like magic.`\n"
            "\n"
            "*Supported Syntax:*  `@jhbjh14514jjhbot <cmd> <terms>`"
            "\n\n"
            "*Example:*    `@jhbjh14514jjhbot !exe idm`",
                parse_mode=ParseMode.MARKDOWN,
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
            "📱 *Mobile Apps Search*\n\n"
            "`You can perform instantaneous app search using any "
            " regex pattern either using the full app name "
            "or by extension. It works like magic.`\n"
            "\n"
            "*Supported Syntax:*  `@jhbjh14514jjhbot <cmd> <terms>`"
            "\n\n"
            "*Example:*    `@jhbjh14514jjhbot !store telegram`",
                parse_mode=ParseMode.MARKDOWN,
                ),
        reply_markup=InlineKeyboardMarkup([[
           
            InlineKeyboardButton(
                "Give it a try",
                switch_inline_query_current_chat="!store telegram"
            )]]),
                description="Learn how to search for software",
                thumb_url=INLINE_HELP_MOBILE_THUMB 
            )
            
            
        ]
          switch_pm_text = "🆘 TELE MULTISTORE HELP"
          if string == "":
            update.inline_query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text="{} Type to search".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
                    switch_pm_parameter="start",
                )
          
      
          things = ["ok"]
          logger.warning('Query "%s"', things)
          try:
            for ft in things:
              su.append(str(ft[3]))
          except IndexError as e:
            articles = INLINE_HELP
            update.inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            offset=offset,
        ) 
            return
      
        
        
        elif query.startswith('!store'): 
          logger.warning(string)
          if string == "":
            update.inline_query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text="{} Type to search Raw Docs".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
                    switch_pm_parameter="start",
                )
          
      
          likeDate = "%" + str(string[7:]) + "%"
          media = "Apps"
          logger.warning(likeDate) 
          c.execute('SELECT DISTINCT DownloadId, Fname, FileId, Media FROM files WHERE Media = ? AND Fname LIKE ? ORDER BY ID DESC LIMIT 100 OFFSET ?', (media, likeDate, offset ))
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
            update.inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            offset=offset,
        ) 
            return
      
          switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.BALLOT_BOX_WITH_BALLOT)
          if things:
            s = 's'
            all = str(su[0])
        
            for num, th in enumerate(things):
              sw.append(str(th[0]))
              articles.append(InlineQueryResultCachedDocument(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=MEDIA_THUMB,document_file_id="{}".format(str(th[2])),
                    description="Click to view the details",
                    caption="{}".format(str(th[1])),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🔄 Send to another Chat", switch_inline_query=str(sw[0]))]
                    ]  
                ))) 
            count = len(articles) - 1
            res = ""
            ress = ""
            if len(str(string[7:])) == 0:
              res = "Items in category" if count > 1 else "Item in category"
            if len(str(string[7:])) >= 1:
              ress = "Results for" if count > 1 else "Result for"
        
            switch_pm_text = "{} Found {} {} \"{}\"".format(Emoji.OPEN_BOOK, count, res if len(str(string[7:])) == 0 else ress, all if len(str(string[7:])) < 1 else str(query[7:]))
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
            switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.OPEN_BOOK, count, s if count > 1 else '', all if strings == "!f" else str(query[7:]))
      
          count = len(articles) - 1
        
        
        
        elif query.startswith('!doc'): 
          logger.warning(string)
          if string == "":
            update.inline_query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text="{} Type to search Raw Docs".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
                    switch_pm_parameter="start",
                )
          
      
          likeDate = "%" + str(string[5:]) + "%"
          media = "Documents"
          logger.warning(likeDate) 
          c.execute('SELECT DISTINCT DownloadId, Fname, FileId, Media FROM files WHERE Media = ? AND Fname LIKE ? ORDER BY ID DESC LIMIT 100 OFFSET ?', (media, likeDate, offset ))
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
            update.inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            offset=offset,
        ) 
            return
      
          switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.BALLOT_BOX_WITH_BALLOT)
          if things:
            s = 's'
            all = str(su[0])
        
            for num, th in enumerate(things):
              sw.append(str(th[0]))
              articles.append(InlineQueryResultCachedDocument(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=MEDIA_THUMB,document_file_id="{}".format(str(th[2])),
                    description="Click to view the details",
                    caption="{}".format(str(th[1])),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🔄 Send to another Chat", switch_inline_query=str(sw[0]))]
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
            switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.OPEN_BOOK, count, s if count > 1 else '', all if strings == "!f" else str(query[7:]))
      
          count = len(articles) - 1
        
        
        
        
        elif query.startswith('!zip'): 
          logger.warning(string)
          if string == "":
            update.inline_query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text="{} Type to search Raw Docs".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
                    switch_pm_parameter="start",
                )
          
      
          likeDate = "%" + str(string[5:]) + "%"
          media = "Archives"
          logger.warning(likeDate) 
          c.execute('SELECT DISTINCT DownloadId, Fname, FileId, Media FROM files WHERE Media = ? AND Fname LIKE ? ORDER BY ID DESC LIMIT 100 OFFSET ?', (media, likeDate, offset ))
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
            update.inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            offset=offset,
        ) 
            return
      
          switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.BALLOT_BOX_WITH_BALLOT)
          if things:
            s = 's'
            all = str(su[0])
        
            for num, th in enumerate(things):
              sw.append(str(th[0]))
              articles.append(InlineQueryResultCachedDocument(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=MEDIA_THUMB,document_file_id="{}".format(str(th[2])),
                    description="Click to view the details",
                    caption="{}".format(str(th[1])),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🔄 Send to another Chat", switch_inline_query=str(sw[0]))]
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
            switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.OPEN_BOOK, count, s if count > 1 else '', all if strings == "!f" else str(query[7:]))
      
          count = len(articles) - 1
        
        
        elif query.startswith('!soft'): 
          logger.warning(string)
          if string == "":
            update.inline_query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text="{} Type to search".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
                    switch_pm_parameter="start",
                )
          
      
          likeDate = "%" + str(string[7:]) + "%"
          media = "Software"
          logger.warning(likeDate) 
          c.execute('SELECT DISTINCT DownloadId, Fname, FileId, Media FROM files WHERE Media = ? AND Fname LIKE ? ORDER BY ID DESC LIMIT 100 OFFSET ?', (media, likeDate, offset ))
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
                    title=str(su[0]).upper(),
                    description="A reliable source for all your desired softwares",
                    input_message_content=InputTextMessageContent(
                        "🖥 *Software Search Tool*\n\n"
                        "`Within this section, you can perform some queries to get your desired software.\n\n regex search is also supported`", parse_mode=ParseMode.MARKDOWN
                    ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Example 1", switch_inline_query_current_chat="!soft idm")],[InlineKeyboardButton("Example 2", switch_inline_query_current_chat="!soft exe")]
                    ]  
                ),
                    thumb_url=SOFTWARE_THUMB,
                )
            )
            
          except IndexError as e:
            articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Nothing has been uploaded so far", thumb_url=NOT_FOUND,
                    description="Try by uploading something first",
                    input_message_content=InputTextMessageContent(
                    "Try uploading something first"
                ))] 
            update.inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            offset=offset,
        ) 
            return
      
          switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.BALLOT_BOX_WITH_BALLOT)
          if things:
            s = 's'
            all = str(su[0])
        
            for num, th in enumerate(things):
              sw.append(str(th[0]))
              articles.append(InlineQueryResultCachedDocument(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=MEDIA_THUMB,document_file_id="{}".format(str(th[2])),
                    description="Click to view the details",
                    caption="{}".format(str(th[1])),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🔄 Send to another Chat", switch_inline_query=str(sw[0]))]
                    ]  
                ))) 
            count = len(articles) - 1
            res = ""
            ress = ""
            if len(str(string[7:])) == 0:
              res = "Items in category" if count > 1 else "Item in category"
            if len(str(string[7:])) >= 1:
              ress = "Results for" if count > 1 else "Result for"
        
            switch_pm_text = "{} Found {} {} \"{}\"".format(Emoji.OPEN_BOOK, count, res if len(str(string[7:])) == 0 else ress, all if len(str(string[7:])) < 1 else str(query[7:]))
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
            switch_pm_text = "{} Found {} Result{} for \"{}\"".format(Emoji.OPEN_BOOK, count, s if count > 1 else '', all if strings == "!f" else str(query[7:]))
      
          count = len(articles) - 1
        
        
        elif query.startswith('!mp3'): 
          logger.warning(string)
          if string == "":
            update.inline_query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text="{} Type to search Raw Docs".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
                    switch_pm_parameter="start",
                )
          
      
          likeDate = "%" + str(string[5:]) + "%"
          media = "Music"
          logger.warning(likeDate) 
          c.execute('SELECT DISTINCT DownloadId, Fname, FileId, Media FROM files WHERE Media = ? AND Fname LIKE ? ORDER BY ID DESC LIMIT 100 OFFSET ?', (media, likeDate, offset ))
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
            update.inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            offset=offset,
        ) 
            return
          switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.BALLOT_BOX_WITH_BALLOT)
          if things:
            s = 's'
            all = str(su[0])
        
            for num, th in enumerate(things):
              sw.append(str(th[0]))
              articles.append(InlineQueryResultCachedAudio(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=MEDIA_THUMB,audio_file_id="{}".format(str(th[2])),
                    description="Click to view the details",
                    caption="{}".format(str(th[1])),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🔄 Send to another Chat", switch_inline_query=str(sw[0]))]
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
            update.inline_query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text="{} Type to search Raw Docs".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
                    switch_pm_parameter="start",
                )
          
      
          likeDate = "%" + str(string[5:]) + "%"
          media = "Video"
          logger.warning(likeDate) 
          c.execute('SELECT DownloadId, Fname, FileId, Media FROM files WHERE Media = ? AND Fname LIKE ? ORDER BY ID DESC LIMIT 100 OFFSET ?', (media, likeDate, offset ))
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
            update.inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            offset=offset,
        ) 
            return
      
          switch_pm_text = "{} TELE MULTISTORE BOT".format(Emoji.BALLOT_BOX_WITH_BALLOT)
          if things:
            s = 's'
            all = str(su[0])
        
            for num, th in enumerate(things):
              sw.append(str(th[0]))
              articles.append(InlineQueryResultCachedVideo(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=MEDIA_THUMB,video_file_id="{}".format(str(th[2])),
                    description="Click to view the details",
                    caption="{}".format(str(th[1])),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🔄 Send to another Chat", switch_inline_query=str(sw[0]))]
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
        
        
        
        
        
        elif len(string) > 0:
          articles = [
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
          ]
          likeDate = "%" + str(query) + "%"
          med = []
          ct = len(med) - 1
          c.execute('SELECT DownloadId, Fname, FileId, Media FROM files WHERE Fname LIKE ? OR DownloadId LIKE ? OR Media LIKE ? ORDER BY ID DESC LIMIT 100 OFFSET ?', (likeDate, likeDate, likeDate,  ct ))
          result = c.fetchall() 
          con.execute("SELECT DISTINCT COUNT (*) FROM files WHERE User = ?", (chat_id, ))  
          
          rowcount = con.fetchone()[0]
          things = [list(i) for i in result]
          
          for ft in things[0:49]:
            su.append(str(ft[3]))
          if things:
            s = 's'
            all = str(su[0])
            for num, th in enumerate(things[0:49]):
              sw.append(str(th[0]))
              med.append(th[3])
              articles.append(InlineQueryResultCachedDocument(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=MEDIA_THUMB,document_file_id="{}".format(str(th[2])),
                    description="Click to view the details",
                    caption="{}".format(str(th[1])),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🔄 Send to another Chat", switch_inline_query=str(sw[0]))]
                    ]  
                ))) 
            count = len(articles) - 1
            rst = len(result)
            res = ""
            ress = ""
            nu = ""
            if len(str(string)) == 0:
              res = "Items in category" if count > 1 else "Item in category"
            if len(str(string)) >= 1:
              ress = "Results for" if count > 1 else "Result for"
            if len(str(string)) >= 1:
              cnts = str(rst)+"+" if rst > 50 else ""
            if len(str(string)) == 0:
              nu = "and "+str(len(all))+" Others" if count > 1 else ""
            switch_pm_text = "{} Found {} {} \"{} {}\"".format(Emoji.OPEN_BOOK, cnts if rst > 50 else count, res if len(str(string)) == 0 else ress, all if len(str(string)) < 1 else str(query), nu)
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
          b = len(articles) - 1
          count = int(round(b/5.0)*5.0)
          update.inline_query.answer(
            results=articles,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            next_offset="" if count <= 48 else offset
        ) 
        else: 
            update.inline_query.answer(
                results=[],
                cache_time=CACHE_TIME,
                switch_pm_text='{} No results for "{}"'.format(Emoji.CROSS_MARK, string),
                switch_pm_parameter="okay",
            )

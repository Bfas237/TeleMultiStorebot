from utils.typing import *
from pyrogram import (
    Emoji, Client, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaDocument 
)
data = {'details': {}, 'download':{}} 
state = {}

 s = 's'
              count = len(articles)
              switch_pm_text = "{} {} Result{} for \"{}\"".format(Emoji.OPEN_BOOK, count, s if count > 1 else '', string)

            query.answer(
                results=articles,
                cache_time=CACHE_TIME,
                switch_pm_text=switch_pm_text,
                switch_pm_parameter="start"
            )
@Client.on_inline_query() 
def answer(client, inline_query):
    query = inline_query.query.lower()
    logger.info(query) 
    chat_id = inline_query.from_user.id
    userd = chat_id 
    not_found = "https://res.cloudinary.com/teepublic/image/private/s--mFvJc027--/t_Resized%20Artwork/c_fit,g_north_west,h_954,w_954/co_ffffff,e_outline:35/co_ffffff,e_outline:inner_fill:35/co_ffffff,e_outline:35/co_ffffff,e_outline:inner_fill:35/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_jpg,h_630,q_90,w_630/v1533147535/production/designs/2966320_0.jpg"
    thumb = "https://cdn4.iconfinder.com/data/icons/modern-education-3/128/118-512.png" 
    articles = []
    sw = []
    if query.startswith('!f'):
      conn = sqlite3.connect('inshorts.db') 
      c = conn.cursor()
      con = conn.cursor()
      likeDate = "%" + str(query[3:]) + "%"
      logger.warning(likeDate) 
      c.execute('SELECT DownloadId, Fname, FileId FROM files WHERE Fname LIKE ? OR DownloadId LIKE ? ORDER BY ID DESC LIMIT 8 OFFSET 0', (likeDate, likeDate ))
      result = c.fetchall() 
      con.execute("SELECT DISTINCT COUNT (*) FROM files WHERE User = ?", (chat_id, ))  
    
      rowcount = con.fetchone()[0]
      things = [list(i) for i in result]
      logger.warning("this is ", things)  
      if things:
        for num, th in enumerate(things):
          sw.append(str(th[0]))
          articles.append(InlineQueryResultArticle(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=thumb,
                    description="Click to view the details",
                    input_message_content=InputTextMessageContent(
                    "{}".format(str(th[1]))
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🔄 Send to another Chat", switch_inline_query="!f "+str(sw[0]))], [InlineKeyboardButton("📥 Instant Download", url="https://telegram.me/jhbjh14514jjhbot?start=dl_"+str(sw[0]))]
                    ]  
                ))) 
      elif not things:
        articles = [InlineQueryResultArticle(
                    id=uuid4(), title="Your search returned Nothing", thumb_url=not_found,
                    description="Try Searching for ("+str(rowcount)+")",
                    input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ))] 
       
      inline_query.answer(articles, cache_time=1, is_personal=True)
      
    
    else:
      inline_query.answer(
        results=[
            InlineQueryResultArticle(
                id=uuid4(),
                title="Installation",
                input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ),
                url="https://docs.pyrogram.ml/start/Installation",
                description="How to install Pyrogram",
                thumb_url="https://i.imgur.com/qhYYqZa.png",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Open website", url="https://docs.pyrogram.ml/start/Installation")]
                    ]
                )
            ),
            InlineQueryResultArticle(
                id=uuid4(),
                title="Usage",
                input_message_content=InputTextMessageContent(
                    "Here's how to use **Pyrogram**"
                ),
                url="https://docs.pyrogram.ml/start/Usage",
                description="How to use Pyrogram",
                thumb_url="https://i.imgur.com/JyxrStE.png",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Open website", url="https://docs.pyrogram.ml/start/Usage")]
                    ]
                )
            )
        ],
        cache_time=1,
            switch_pm_text="{} Type to search your storage".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
            switch_pm_parameter="start"
    )









from utils.typing import *
from pyrogram import (
    Emoji, Client, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaDocument 
)
data = {'details': {}, 'download':{}} 
state = {}
import logging
logging.getLogger("pyrogram").setLevel(logging.WARNING)
NEXT_OFFSET = 25
CACHE_TIME = 5

FIRE_THUMB = "https://i.imgur.com/qhYYqZa.png"
ROCKET_THUMB = "https://i.imgur.com/PDaYHd8.png"
OPEN_BOOK_THUMB = "https://i.imgur.com/v1XSJ1D.png"


@Client.on_inline_query() 
def answer(client, inline_query):
    query = inline_query.query
    logger.warning(query) 
    chat_id = inline_query.from_user.id
    userd = chat_id 
    sw = []
    not_found = "https://res.cloudinary.com/teepublic/image/private/s--mFvJc027--/t_Resized%20Artwork/c_fit,g_north_west,h_954,w_954/co_ffffff,e_outline:35/co_ffffff,e_outline:inner_fill:35/co_ffffff,e_outline:35/co_ffffff,e_outline:inner_fill:35/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_jpg,h_630,q_90,w_630/v1533147535/production/designs/2966320_0.jpg"
    thumb = "https://cdn4.iconfinder.com/data/icons/modern-education-3/128/118-512.png" 
    DEFAULT_RESULTS = [
            InlineQueryResultArticle(
                id=uuid4(),
                title="Usage",
                input_message_content=InputTextMessageContent(
            "{} **Tele MultiStore**\n\n"
            "Tele MultiStore is an advanced, easy-to-use Telegram bot that replaces keeps track of all "
            "your uploaded files either through forwading, uploading "
            "or downloading from the web.".format(Emoji.CARD_INDEX_DIVIDERS),
                ),
                description="How to use Pyrogram",
                thumb_url="https://i.imgur.com/JyxrStE.png"
            )
        ]
    string = inline_query.query.lower()
    
    if string == "":
        inline_query.answer(
            results=DEFAULT_RESULTS,
            cache_time=CACHE_TIME,
            switch_pm_text="{} Type to search your storage".format(Emoji.MAGNIFYING_GLASS_TILTED_RIGHT),
            switch_pm_parameter="start",
        )

        return

    results = []
    offset = int(inline_query.offset or 0)
    switch_pm_text = "{} Tele MultiStore".format(Emoji.OPEN_FILE_FOLDER)

    if string == "!m":
      conn = sqlite3.connect('inshorts.db') 
      c = conn.cursor()
      con = conn.cursor()
      con.execute("SELECT DISTINCT COUNT (*) FROM files WHERE User = ?", (chat_id, ))  
    
      rowcount = con.fetchone()[0]
       
      switch_pm_text = "{} Media Finder ({})".format(Emoji.CLOSED_BOOK, rowcount)
      qur = string[3:]
      logger.info(qur)
      if offset == 0:
            results.append(
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
          
              
            likeDate = "%" + str(query[3:]) + "%"
            c.execute('SELECT DownloadId, Fname, FileId FROM files WHERE Fname LIKE ? OR DownloadId LIKE ? ORDER BY ID DESC LIMIT 8 OFFSET 0', (likeDate, likeDate ))
            result = c.fetchall() 
            things = [list(i) for i in result]
            
            if things:
              for num, th in enumerate(things):
                sw.append(str(th[0]))
                results.append(InlineQueryResultArticle(
                    id=uuid4(), title="("+str(num)+") - {}".format(str(th[1])), thumb_url=thumb,
                    description="Click to view the details",
                    input_message_content=InputTextMessageContent(
                    "{}".format(str(th[1]))
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🔄 Send to another Chat", switch_inline_query="!f "+str(sw[0]))], [InlineKeyboardButton("📥 Instant Download", url="https://telegram.me/jhbjh14514jjhbot?start=dl_"+str(sw[0]))]
                    ]  
                ))) 
            elif not things:
              results = [InlineQueryResultArticle(
                    id=uuid4(), title="Your search returned Nothing", thumb_url=not_found,
                    description="Try Searching for ("+str(rowcount)+")",
                    input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ))] 

    if results:
        inline_query.answer(
            results=results,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            next_offset=str(offset + NEXT_OFFSET),
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
            
        else:
            inline_query.answer(
                results=[],
                cache_time=CACHE_TIME,
                switch_pm_text='{} No results for "{}"'.format(Emoji.CROSS_MARK, string),
                switch_pm_parameter="okay",
            )



  
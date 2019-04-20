from pyrogram import Client, Filters
import logging, os
from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("telegram").setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
plugins = dict(
    root="plugins"
)
from plugins.inlines.inline import *
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('"%s" %s"', update, context.error)

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(os.environ.get("TOKEN"), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(answer_inline))
    
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    Client("mybot", bot_token=os.environ.get("TOKEN"), api_id=os.environ.get("api_id"), api_hash=os.environ.get("api_hash"), plugins=plugins).run()
    updater.idle()


if __name__ == "__main__" :
    main()
    
      

from utils.typing import *
from utils.menus import *
import subprocess    

class Translation(object):
    START_TEXT = "Welcome to our bot. I am capable of downloading your best apps within seconds. \n\nI can do some basic functions for now which you can discover by navigating by yourself. Hope you find me useful 😊\n\nFor more help use the help button or just send /help\n\n"
    ABS_TEXT = " Please don't be selfish."
    UPGRADE_TEXT = "No upgrades!"
    NOT_AUTH_USER_TEXT = "The bot developer is a selfish dude. for now you can\'t download anything for this is just the beta bot. try the main bot at @gmotherbot"
    CUSTOM_CAPTION_UL_FILE = " © @Bfas237Bots"
  
    SAVED_RECVD_DOC_FILE = "Document Downloaded Successfully."
    REPLY_TO_DOC_GET_LINK = "Reply to a Telegram media to get High Speed Direct Download Link"
    FILETRANSFER_GET_DL_LINK = "Filetransfer.sh Direct Link <a href='{}'>Generated</a> valid for {} days.\n\nFile.io Direct Link <a href='{}'>Generated</a> valid for {} days.\n\nanonfile.com Direct Link <a href='{}'>Generated</a> valid for ^^ days.\n\n© @bfas237bots"
    
    DOWNLOAD_START = "**⏳ Initializing Your request**..."
    UPLOAD_START = "**⬆️ Uploading to external file hosting**"
    SERVICES = "<b>Services Used by </b> @APKFetcherBot\n\n🔋 <a href='https://docs.pyrogram.ml/'>Pyrogram</a> - For Ultra fast download speed\n\n🔋 <a href='https://transfer.sh/'>Transfer.sh</a> - For External File Hosting\n\n🔋 <a href='https://www.file.io/'>File.io</a> - For External File Hosting\n\n🔋 <a href='http://bsbe.cf/'>bsbe.cf</a> - Trimming your long links"
active_chats = {}
@Client.on_message(Filters.command("link"))
def ft(bot, update):
    global active_chats
    start = time.time()
    if update.from_user.id not in active_chats:
        active_chats[update.from_user.id] = {'actions': []}
    active_chats[update.from_user.id]['actions'].append('filetransfer')
    if update.reply_to_message is not None: 
        logger.warning('Downloading with filetransfer')
        reply_message = update.reply_to_message
        required_file_name = "{}/.data".format(os.getcwd())
        download_location = required_file_name + "/"
        a = update.reply(Translation.DOWNLOAD_START,
            quote=True
        ) 
        after_download_file_name = bot.download_media(
            message=reply_message,
            file_name=download_location, progress = DFromUToTelegramProgress, progress_args = (a, update.chat.id, start, "**📥 Downloading:**")
        )
        filename_w_ext = os.path.basename(after_download_file_name)
        filename, download_extension = os.path.splitext(filename_w_ext)
        filename = filename.strip('\n').replace(' ','_')
        bot.edit_message_text(
            text=Translation.SAVED_RECVD_DOC_FILE,
            chat_id=update.from_user.id,
            message_id=a.message_id
        )
        url = "https://transfer.sh/{}{}".format(str(filename), str(download_extension))
        max_days = "7"
        command_to_exec = [
            "curl",
            # "-H", 'Max-Downloads: 1',
            "-H", 'Max-Days: 7', # + max_days + '',
            "--upload-file", after_download_file_name,
            url
        ]
        a.edit(Translation.UPLOAD_START
        )
        expires = "1w"
        
        url = "https://file.io/?expires={expires}"
        fin = open(after_download_file_name, 'rb')
        files = {'file': fin}
        try:
            max_days = "7"
            r = requests.post(url, files=files).json()
            print(r['link'])
            urls = " https://anonfile.com/api/upload"
            rs = requests.post(urls, files=files).json()
            print(rs['data']['file']['url']['short']) 
            logger.info(command_to_exec)
            t_response = subprocess.check_output(command_to_exec, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            logger.info("Status : FAIL", exc.returncode, exc.output)
            bot.edit_message_text(
                chat_id=update.from_user.id,
                text=exc.output.decode("UTF-8"),
                message_id=a.message_id
            )
        except:
                bot.edit_message_text(
                chat_id=update.from_user.id,
                text="Error uploading file",
                message_id=a.message_id
            )
                os.remove(after_download_file_name)
                pass
       
        else:
            
            t_response_arry = t_response.decode("UTF-8").split("\n")[-1].strip()
            bot.edit_message_text(
                chat_id=update.from_user.id,
                text=Translation.FILETRANSFER_GET_DL_LINK.format(t_response_arry, max_days,r['link'], max_days, rs['data']['file']['url']['short']),
                parse_mode="HTML",
                message_id=a.message_id,
                disable_web_page_preview=True
            ) 
        
       
        finally:
            os.remove(after_download_file_name)
            fin.close()
            pass
    else:
        bot.send_message(
            chat_id=update.from_user.id,
            text=Translation.REPLY_TO_DOC_GET_LINK,
            reply_to_message_id=update.message_id
        )
    
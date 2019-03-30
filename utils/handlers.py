from utils.typing import *
import mimetypes
import mimetypes, magic, math
from fake_useragent import  UserAgent  
import time
download_path = "{}/Downloads".format(os.getcwd())
if not os.path.isdir(download_path):
  os.makedirs(download_path)
print(download_path)   

def Search(query): 
    session = requests.Session()
    opt={}
    data = {'details': {}, 'download':{}}
    base = {
        'User-Agent':  'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch, ',
        'Accept-Language': 'zh-CN,zh,en-US,en,fr,fr-FR;q=0.8,ta;q=0.6',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive' 
    }
    heads = dict(base, **opt)
    response = session.get('https://www.filehorse.com/search?q={}'.format(quote_plus(query)), headers=heads).text  
    soup = BeautifulSoup(response, "html.parser")
    g = [] 
    result = []
    nu = []
    seen = set()
    seens = set()
    links = []
    go = []
    gos = [] 
    f = []
    gu = []
    s = []
    for j in soup.findAll('ul', {'class':'software_list'}):
      for li in j.findAll('li'):  
        
        try:
          for h3 in li.findAll('h3'):   
            for href in li.findAll('a'):
              title = h3.text 
              link = href['href']   
              
              g.append((title, link))  
            for item in g:
              if item not in seen:
                seen.add(item)
                result.append(item)
            if len(result) > 0:
              items = ""
              for idx, app in enumerate(result):  
                items = "{}|{}".format(idx, app)  
                links.append(app[1])
                nu.append(items)
              for url in links:
                response = session.get(url, headers=headers).text
                
                det = BeautifulSoup(response, "html.parser") 
                i = det.find('div', attrs={'class':'main_down_link'})
                href = i.find('a')['href']
                ty = i.find('a').text
                data['download'][ty]=href 
                data['title'] = h3.text
                data['link'] = url
                for j in det.findAll('ul', {'class':'software_facts'}):
                  for li in j.findAll('li'):
                    children = li.findChildren("p" , recursive=False) 
                    for child in children: 
                      gu.append(child.text)
                  data['details'] = gu
              
              f.append(data) 
                    
        except AttributeError: 
            pass
    return data           
#d = Search("whatsapp")
"""for i, (k, v) in enumerate(d.items()):
    print(list(enumerate(d.items()))) 
    print(d['link'])"""   
     
 
  
def ApkDownload(link, client, message_id, chat_id, *current, **total):
    base_headers = {
        'User-Agent':  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5',
        'Accept-Encoding': 'gzip, deflate, sdch, ',
        'Accept-Language': 'zh-CN,zh,en-US,en,fr,fr-FR;q=0.8,ta;q=0.6',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive'
    } 
        
    headers = dict(base_headers, **options)
    res = requests.get(link + '/download?from=details', headers=headers).text
    soup = BeautifulSoup(res, "html.parser").find('a', {'id':'download_link'})
    valid = False
    if soup['href']:
        r = requests.get(soup['href'], stream=True, allow_redirects=True, headers=headers)
        required_file_nam = get_filename_from_cd(r.headers.get('content-disposition'))
        required_file_name = required_file_nam.strip('\n').replace('\"','').replace('\'','').replace('?','').replace(" ", "_")
        title, ext = splitext(basename(required_file_name))
        title = title.replace('_',' ').replace('-','').replace('@',' ').replace("#", " ").strip("\ apkpure.com").replace("\ apkpure.com", "")
        with open(required_file_name, 'wb') as file:
          total_length = int(r.headers.get('content-length', 0)) or None
          downloaded_size = 0
          chunk_size=8192*1024
          if total_length is None:  # no content length header
            file.write(r.content)
          else:
            dl = 0
            total_length = int(total_length)
            for chunk in r.iter_content(chunk_size=chunk_size):
              if chunk:
                  dl += len(chunk)
                  done = int(100 * dl / total_length)
                  file.write(chunk)
                  file.flush()
                  os.fsync(file.fileno())
                  downloaded_size += chunk_size
                  if ((total_length // downloaded_size) % 5) == 0:
                    try:
                      file_size = os.stat(file_name).st_size
                      client.send_chat_action(chat_id,'UPLOAD_DOCUMENT') 
                      message_id.edit("**⬇️ Downloading:** {}% of {}".format(humanbytes(downloaded_size),
                                humanbytes(total_length)))
                      
                    except: 
                      pass
        
    else:
        message_id.edit("No valid Download link was found.\n\n The server terminated all request. Kindly try again")
        
        
        
    return required_file_nam, title, total_length
                        
                        
def SizeFormatter(b: int,
                  human_readable: bool = False) -> str:
    """
    Adjust the size from bits to the right measure.

    b (``int``): Number of bits.


    SUCCESS Returns the adjusted measure (``str``).
    """
    if human_readable:
        B = float(b / 8)
        KB = float(1024)
        MB = float(pow(KB, 2))
        GB = float(pow(KB, 3))
        TB = float(pow(KB, 4))

        if B < KB:
            return "{0} B".format(B)
        elif KB <= B < MB:
            return "{0:.2f} KB".format(B/KB)
        elif MB <= B < GB:
            return "{0:.2f} MB".format(B/MB)
        elif GB <= B < TB:
            return "{0:.2f} GB".format(B/GB)
        elif TB <= B:
            return "{0:.2f} TB".format(B/TB)
    else:
        B, b = divmod(int(b), 8)
        KB, B = divmod(B, 1024)
        MB, KB = divmod(KB, 1024)
        GB, MB = divmod(MB, 1024)
        TB, GB = divmod(GB, 1024)
        tmp = ((str(TB) + "TB, ") if TB else "") + \
            ((str(GB) + "GB, ") if GB else "") + \
            ((str(MB) + "MB, ") if MB else "") + \
            ((str(KB) + "KB, ") if KB else "") + \
            ((str(B) + "B, ") if B else "") + \
            ((str(b) + "b, ") if b else "")
        return tmp[:-2]


def TimeFormatter(milliseconds: int) -> str:
    """
    Adjust the time from milliseconds to the right measure.

    milliseconds (``int``): Number of milliseconds.


    SUCCESS Returns the adjusted measure (``str``).
    """
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

def DFromUToTelegramProgress(client,
                             current,
                             total,
                             msg,
                             chat_id,
                             start) -> None:
    """
    Use this method to update the progress of a download from/an upload to Telegram, this method is called every 512KB.
    Update message every ~4 seconds.

    client (:class:`Client <pyrogram.Client>`): The Client itself.

    current (``int``): Currently downloaded/uploaded bytes.

    total (``int``): File size in bytes.

    msg (:class:`Message <pyrogram.Message>`): The Message to update while downloading/uploading the file.

    chat_id (``int`` | ``str``): Unique identifier (int) or username (str) of the target chat. For your personal cloud (Saved Messages) you can simply use "me" or "self". For a contact that exists in your Telegram address book you can use his phone number (str). For a private channel/supergroup you can use its *t.me/joinchat/* link.

    text (``str``): Text to put into the update.

    start (``str``): Time when the operation started.


    Returns ``None``.
    """
    # 1048576 is 1 MB in bytes
    text = "**⌛️ Uploading:**"
    now = time.time()
    diff = now - start
    if round(diff % 4.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
        # 0% = [░░░░░░░░░░░░░░░░░░░░]
        # 100% = [████████████████████]
        progress = "[{0}{1}] {2}%\n".format(''.join(["█" for i in range(math.floor(percentage / 5))]),
                                            ''.join(
            ["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))
        tmp = progress + "\n**Running:** {0}/{1}\n\n**Speed:** {2}/s \n\n**Estimated Time:** {3}/{4}\n".format(SizeFormatter(b=current * 8,
                                                                         human_readable=True),
                                                           SizeFormatter(b=total * 8,
                                                                         human_readable=True),
                                                           SizeFormatter(b=speed * 8,
                                                                         human_readable=True),
                                                           elapsed_time if elapsed_time != '' else "0 s",
                                                           estimated_total_time if estimated_total_time != '' else "0 s")

        msg.edit(text=text + tmp)
common_words = frozenset(("if", "but", "and", "the", "when", "use", "to", "for"))
title = "When to use Python for web applications"
title_words = set(title.lower().split())
keywords = title_words.difference(common_words)
def mime_content_type(url, content_type, name):
    """Get mime type
    :param filename: str
    :type filename: str
    :rtype: str
    """
    
    filenam = basename(name)
    
    exts = os.path.splitext(filenam)[1][1:].lower()
    if exts:
      exts = "."+exts
    else:
      exts = None
      logger.warning("No filetype could be determined for '%s', skipping.",
            filenam
        )
      
    
    if exts in common_types or exts in types_map: 
        ext = '{}'.format(exts)
        mime_typ = '{}'.format(types_map[exts])
        print(ext) 
        print(mime_typ)
      
    elif content_type == 'image/jpeg' or content_type == 'image/jpg' or content_type == 'image/jpe':
            ext = '.jpeg'
        
    elif content_type == 'image/x-icon' or content_type == 'image/vnd.microsoft.icon':
            ext = '.ico'
        
    elif content_type == 'application/x-7z-compressed':
            ext = '.7z'
    elif content_type == 'image/png':
            ext = '.png'
        
    elif None == exts:
        ext = mimetypes.guess_extension(content_type)
        logger.warning("No extension for '%s', guessed '%s'.",
        filenam, ext
                  )
        
        print(ext)
    ent = ext

    if ent in common_types or ent in types_map: 
        print ('File Extenstion: {} has MIME Type: {}.'.format(ent, types_map[ent]))
    return ext
def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_filename(url):
    """
    Does the url contain a downloadable resource
    """
    request = urllib.request.Request(url, headers=req_headers)
    opener = urllib.request.build_opener()
    response = opener.open(request)
    code = response.code
    headers = response.headers
    if code < 400:
       disassembled = urlparse(url)
       filenam, file_ext = splitext(basename(disassembled.path))
       if(filenam != None):
         filename = unquote(filenam).strip('\n').replace('\"','').replace('\'','').replace('?','').replace(" ", "_")
         ext = file_ext
         
       else:
         filename = None
         ext = None
        
    return filename, ext
def dynamic_data(data):
    return Filters.create(
        name="DynamicData",
        func=lambda filter, callback_query: filter.data == callback_query.data,
        data=data  # "data" kwarg is accessed with "filter.data"
    )

def fileExt(url):
    """
    Check if file extention exist then
    
    """
    # compile regular expressions
    reQuery = re.compile(r'\?.*$', re.IGNORECASE)
    rePort = re.compile(r':[0-9]+', re.IGNORECASE)
    reExt = re.compile(r'(\.[A-Za-z0-9]+$)', re.IGNORECASE)

    # remove query string
    url = reQuery.sub("", url)

    # remove port
    url = rePort.sub("", url)

    # extract extension
    matches = reExt.search(url)
    if None != matches:
        return matches.group(1)
    return None
def get_filename(url):
    """
    Get an authentique filename from content-dispostion
    """
    
# content-disposition = "Content-Disposition" ":"
#                        disposition-type *( ";" disposition-parm )
# disposition-type    = "inline" | "attachment" | disp-ext-type
#                     ; case-insensitive
# disp-ext-type       = token
# disposition-parm    = filename-parm | disp-ext-parm
# filename-parm       = "filename" "=" value
#                     | "filename*" "=" ext-value
# disp-ext-parm       = token "=" value
#                     | ext-token "=" ext-value
# ext-token           = <the characters in token, followed by "*">
    result = requests.get(url, allow_redirects=True)
    code = result.status_code
    headers = result.headers
    if code < 400:
      token = '[-!#-\'*+.\dA-Z^-z|~]+'
      qdtext='[]-~\t !#-[]'
      mimeCharset='[-!#-&+\dA-Z^-z]+'
      language='(?:[A-Za-z]{2,3}(?:-[A-Za-z]{3}(?:-[A-Za-z]{3}){,2})?|[A-Za-z]{4,8})(?:-[A-Za-z]{4})?(?:-(?:[A-Za-z]{2}|\d{3}))(?:-(?:[\dA-Za-z]{5,8}|\d[\dA-Za-z]{3}))*(?:-[\dA-WY-Za-wy-z](?:-[\dA-Za-z]{2,8})+)*(?:-[Xx](?:-[\dA-Za-z]{1,8})+)?|[Xx](?:-[\dA-Za-z]{1,8})+|[Ee][Nn]-[Gg][Bb]-[Oo][Ee][Dd]|[Ii]-[Aa][Mm][Ii]|[Ii]-[Bb][Nn][Nn]|[Ii]-[Dd][Ee][Ff][Aa][Uu][Ll][Tt]|[Ii]-[Ee][Nn][Oo][Cc][Hh][Ii][Aa][Nn]|[Ii]-[Hh][Aa][Kk]|[Ii]-[Kk][Ll][Ii][Nn][Gg][Oo][Nn]|[Ii]-[Ll][Uu][Xx]|[Ii]-[Mm][Ii][Nn][Gg][Oo]|[Ii]-[Nn][Aa][Vv][Aa][Jj][Oo]|[Ii]-[Pp][Ww][Nn]|[Ii]-[Tt][Aa][Oo]|[Ii]-[Tt][Aa][Yy]|[Ii]-[Tt][Ss][Uu]|[Ss][Gg][Nn]-[Bb][Ee]-[Ff][Rr]|[Ss][Gg][Nn]-[Bb][Ee]-[Nn][Ll]|[Ss][Gg][Nn]-[Cc][Hh]-[Dd][Ee]'
      valueChars = '(?:%[\dA-F][\dA-F]|[-!#$&+.\dA-Z^-z|~])*'
      dispositionParm = '[Ff][Ii][Ll][Ee][Nn][Aa][Mm][Ee]\s*=\s*(?:({token})|"((?:{qdtext}|\\\\[\t !-~])*)")|[Ff][Ii][Ll][Ee][Nn][Aa][Mm][Ee]\*\s*=\s*({mimeCharset})\'(?:{language})?\'({valueChars})|{token}\s*=\s*(?:{token}|"(?:{qdtext}|\\\\[\t !-~])*")|{token}\*\s*=\s*{mimeCharset}\'(?:{language})?\'{valueChars}'.format(**locals())

      try:
        m = re.match('(?:{token}\s*;\s*)?(?:{dispositionParm})(?:\s*;\s*(?:{dispositionParm}))*|{token}'.format(**locals()), result.headers['Content-Disposition'])

      except KeyError:
        name = path.basename(unquote(urlparse(url).path))

      else:
        if not m:
          name = path.basename(unquote(urlparse(url).path))

  # Many user agent implementations predating this specification do not
  # understand the "filename*" parameter.  Therefore, when both "filename"
  # and "filename*" are present in a single header field value, recipients
  # SHOULD pick "filename*" and ignore "filename"

        elif m.group(8) is not None:
          name = urllib.unquote(m.group(8)).decode(m.group(7))

        elif m.group(4) is not None:
          name = urllib.unquote(m.group(4)).decode(m.group(3))

        elif m.group(6) is not None:
          name = re.sub('\\\\(.)', '\1', m.group(6))

        elif m.group(5) is not None:
          name = m.group(5)

        elif m.group(2) is not None:
          name = re.sub('\\\\(.)', '\1', m.group(2))

        else:
          name = m.group(1)

  # Recipients MUST NOT be able to write into any location other than one to
  # which they are specifically entitled

        if name:
          name = path.basename(name)

        else:
          name = path.basename(unquote(urlparse(url).path))
          
        name = unquote(name).strip('\n').strip('\*').replace('UTF-8', "").strip('\=').replace('\"','').replace('\'','').replace('?','').replace(" ", "_")
      
      filenam, ext = splitext(basename(name))
      if ext:
        ext = fileExt(url)
      else:
        content_type = headers['content-type']
        ext = mime_content_type(url, content_type, name)
    return filenam, ext
def generate_uuid():
        random_string = ''
        random_str_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        uuid_format = [8]
        for n in uuid_format:
            for i in range(0,n):
                random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])
            if n != 8:
                random_string += '-' 
        return random_string.strip('\n').replace('\"','').replace('\'','').replace('?','').replace(" ", "_")
def human_readable_bytes(bytes):
        KB = 1024
        MB = 1024 * 1024
        GB = MB * 1024

        if bytes >= KB and bytes < MB:
            result = bytes / KB
            converted = 'KB'
        elif bytes >= MB and bytes < GB:
            result = bytes / MB
            converted = 'MB'
        elif bytes >= GB:
            result = bytes / GB
            converted = 'GB'
        else:
            result = bytes
            converted = 'byte'

        result = "%.1f" % result
        results = (
            str(result) + ' ' + converted,
            result,
            converted
        )

        return results
def pretty_size(sizes):
    units = ['B', 'KB', 'MB', 'GB']
    unit = 0
    while sizes >= 1024:
        sizes /= 1024
        unit += 1
    return '%0.2f %s' % (sizes, units[unit])
def dosomething(buf):
    """Do something with the content of a file"""
    sleep(0.01)
    pass
from requests.exceptions import RequestException

def prog(client, current, total, message_id, chat_id, required_file_name):
 if round(current/total*100, 0) % 5 == 0:
  try:
   file_size = os.stat(required_file_name).st_size
   client.send_chat_action(chat_id,'UPLOAD_DOCUMENT')
   message_id.edit("**⬆️ Uploading:** {}% of {}".format(round(current/total*100, 0), str(pretty_size(file_size)))
   )
 
  except:
   pass
         

from pyrogram.api.errors import (
    BadRequest, Flood, InternalServerError,
    SeeOther, Unauthorized, UnknownError
)      
def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd: 
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]
options={}
base_headers = {   
        'User-Agent':  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.5',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
headers = dict(base_headers, **options) 

def DownL(url):
    fname, ext = get_filename(url)
    file_name = fname+ext
    r = requests.get(url, stream=True, allow_redirects=True, headers=headers)
    with open(file_name, 'wb') as file:
      total_length = r.headers.get('content-length')
      if total_length is None:  # no content length header
        file.write(r.content)
      else:
        dl = 0
        total_length = int(total_length)
        for chunk in progress.bar(r.iter_content(chunk_size=8192*1024), expected_size=(total_length / 1024) + 1):
          if chunk:
            dl += len(chunk)
            done = int(100 * dl / total_length)
            file.write(chunk)
            file.flush()
            os.fsync(file.fileno())

def DownLoadFile(url, file_name, client, message_id, chat_id):
    r = requests.get(url, stream=True, allow_redirects=True, headers=headers)
    fname, ext = get_filename(url)
    file_name = fname+ext
    
    with open(download_path+"/"+file_name, 'wb') as file:
      total_length = int(r.headers.get('content-length', 0)) or None
      downloaded_size = 0
      chunk_size=8192*1024
      if total_length is None:  # no content length header
        file.write(r.content)
      else:
        start = time.time()
        dl = 0
        total_length = int(total_length)
        if total_length > 10000000:
          file_name = 0
          return file_name
        for chunk in progress.bar(r.iter_content(chunk_size=chunk_size), expected_size=(total_length / 1024) + 1):
          if chunk:
            dl += len(chunk)
            file.write(chunk)
            done = int(100 * dl / total_length)
            downloaded_size += chunk_size
            DFromUToTelegramProgress(client, dl, total_length, message_id, chat_id, start)
            file.flush()
            os.fsync(file.fileno())
    return file_name
  
  
  
  
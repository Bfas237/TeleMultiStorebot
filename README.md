
# Tele MultiStore Bot
[![LIBRARY](https://img.shields.io/badge/Telegram%20MTProto%20API%20Framework%20for%20Python-April%2005%2C%202019-36ade1.svg)](https://docs.pyrogram.ml)
![PYTHON](https://img.shields.io/badge/Python-%3E%3D3.4-8892bf.svg)


> An advanced [Telegram Bot](http://t.me/TeleMultiStoreBot) for uploading and sharing mdeia files across chats.    
> (Almost) Complete but for now its still in BETA stage.

Requirements
---------

* Python >=3.5
* Telegram account.
* Telegram API key, you can get one simply with [@BotFather](https://core.telegram.org/bots#botfather) with simple commands right after creating your bot.

Dependencies
---------
- Pyrogram 
- requests
- TgCrypto
- bs4
- clint
- python-magic
- timeago


Normal Installation
---------

There are two possible was of running this bot.

##### 1. Using the ini file

* Replace the values as specified [HERE](https://docs.pyrogram.ml/start/Setup#api-keys).

Your final ini file should look like this

```
[pyrogram]
api_id = 12345
api_hash = 0123456789abcdef0123456789abcdef

[plugins]
root = plugins

```

##### 2. ENV variables

To achieve this, you will do as follows. 

> If you use Heroku then this will be very easy to understand

create env variables as the one below

```
TOKEN="123456789:hdhdhdbhfjfkrp889g8g889"
APP_ID=12345
API_HASH="0123456789abcdef0123456789abcdef"

```
* Learn more about how to create and [deploy apps to Heroku](https://devcenter.heroku.com/articles/git#for-a-new-heroku-app)


The Hard Way (Advanced users only)
---------

```sh
virtualenv -p python3 VENV
. ./VENV/bin/activate
pip3 install -r requirements.txt
```


### Run Bot

```
python3 bot.py

```


Easy Installation and Deploy
---------

> This section covers the case where someone is unfamiliar with python in deeper sense. If you are that type then this section has been made purposely for you.

> We are not spoonfeeding you but just making things easier. Read this carefully


If you don't want to go through all those hard process then just click the button below and fill the fields as specified.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Bfaschat/TeleMultiStorebot/tree/glitch)



## Features to be Added:

- [x] Cancel a particular Download
- [x] Alert whether Download was started or not
- [x] Show the available download speed of the server
- [ ] Decrypt and encrypt files with passwords
- [ ] Unarchive archivable files
- [ ] Download torrens



## Screenshots

> To be updated.....


Contact me
------------
You can contact me [via Telegram](https://telegram.me/bfaschat) but if you have an issue please [open](https://github.com/Bfaschat/TeleMultiStorebot/issues) one.



[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://github.com/Bfaschat/TeleMultiStorebot)
[![forthebadge](https://forthebadge.com/images/badges/for-you.svg)](https://github.com/Bfaschat/TeleMultiStorebot)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://github.com/Bfaschat/TeleMultiStorebot) 



# Tele MultiStore Bot
[![LIBRARY](https://img.shields.io/badge/Advanced%20Multipurpose%20Telegram%20Store%20Bot-V0.04-36ade1.svg)](https://docs.pyrogram.ml)
![PYTHON](https://img.shields.io/badge/Python-%3E%3D3.5-8892bf.svg)


> An advanced Multipurpose [Telegram Bot](http://t.me/TeleMultiStoreBot) for uploading and sharing mdeia files across chats. 
> Supports Inline Mode for quciker and better compatibility
> (Almost) Complete but for now its still in BETA stage.

Requirements
---------

* Python >=3.5
* Telegram account.
* Telegram API key, you can get one simply with [@BotFather](https://core.telegram.org/bots#botfather) with simple commands right after creating your bot.
* Your own `API_ID` and `API_HASH` [HOW TO GET MY API CREDENTIALS](https://docs.pyrogram.ml/start/Setup.html#api-keys)
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


## Supported Features 


- [x] Search using inline mode for any uploaded file
- [x] search your storage through Inline Mode
- [x] Asynchronous File Storage
- [x] Lock and unlock Files
- [x] Download and upload with progress bar
- [x] Sort Files according to Media Types

## Features to be Added:

- [ ] Cancel a particular Download
- [ ] Decrypt and encrypt files with passwords
- [ ] Unarchive archivable files
- [ ] Download torrens



## Screenshots

> To be updated.....


Contact me
------------
You can contact me [via Telegram](https://telegram.me/bfaschat) but if you have an issue please [open](https://github.com/Bfaschat/TeleMultiStorebot/issues) one.


Contributing
------------

Tele MultiStore is brand new, and *you are welcome to try it and help make it even better* by either submitting pull requests or reporting issues/bugs as well as suggesting best practices, ideas, enhancements on both code and documentation. Any help is appreciated!



[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://github.com/Bfaschat/TeleMultiStorebot)
[![forthebadge](https://forthebadge.com/images/badges/for-you.svg)](https://github.com/Bfaschat/TeleMultiStorebot)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://github.com/Bfaschat/TeleMultiStorebot) 


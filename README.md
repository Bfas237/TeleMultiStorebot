![HEADER](screenshots/header.png)

A Web App to Start a file download remotely on the server. Server is hosted using [ngrok](https://ngrok.com/) and connecting it to a Telegram Bot can notify about server activities

# Uses
1. Could be used by college students who have limited internet access in their colleges to remotely put stuff to download on a server hosted at home(tv shows and stuff).
2. Put stuff to download on home servers on the go.

## How to Start ?

#### Dependencies:
1. Flask
2. Wget (built-in in linux, need to install on windows)
3. Python 3

The server is started hosted ngrok. When the server starts, a message with the url is sent to the Telegram bot **@downloadgator_bot** (Download Telegram from Google Playstore)

**Add your telegram user id in the `main.py` file on line 65, else it won't work.**
**You can get your id from the @get_id_bot in Telegram**

1.   Read more about setting up ngork on [ngrok](https://ngrok.com/)
2.   Make the `start_server.sh` file executable and run with `./start_server.sh` or
2.   Run `sh start_server.sh`

To clear the `Downloads/` folder and reset the `Downloads/downloads.json` file, run the `reset_downloads.sh` file on the server by either
1.  `sh reset_downloads.sh`  or
2.  `./reset_downloads.sh` (make it executable before running)




## Features to be Added:

- [ ] Cancel a particular Download
- [ ] Alert whether Download was started or not
- [ ] Show the available download speed of the server

## Screenshots

> ![Main](screenshots/a.png)


> ![Main](screenshots/b.png)


> ![Main](screenshots/c.png)


> ![Main](screenshots/d.png)

### Telegram Bot
> <img src="screenshots/e.png" width="400px">


[![forthebadge](https://forthebadge.com/images/badges/for-you.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-javascript.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) 
[![forthebadge](https://forthebadge.com/images/badges/uses-html.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/uses-css.svg)](https://forthebadge.com)

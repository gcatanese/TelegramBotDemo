# TelegramBotDemo
Simple Telegram Bot

Find here the source code of the [Advanced Telegram Chatbots: features that make a difference](https://towardsdatascience.com/bring-your-telegram-chatbot-to-the-next-level-c771ec7d31e4) 
article.

## Setup

Clone the repository

```
git clone https://github.com/gcatanese/TelegramBotDemo.git
```

Create and *.env* file in the same folder as *app.py*. The *.env* file defines the environment variables.  

* TELEGRAM_TOKEN={your Telegram token}


## Run on Local
Run the application
```
cd telegram_bot
python telegram_bot.py
```
Access the bot via the deeplink `https://t.me/{bot_username}` and start chatting

**Note**: the chatbot runs in Polling mode

## Deploy to Heroku

### Prerequisites
* [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
* `requirements.txt` must be in the root folder, it defines the required dependencies
* `runtime.txt` must be in the root folder, it sets the Python version
* `Procfile` must be in the root folder, it declares the startup command

### Create and Configure the Heroku app

Create a new app 
 
```
heroku create advancedtelegrambot
```

Check the remote is correct
```
git remote -v
```
**Note**: the remote is called `heroku` by default but it can be renamed

Define the Python buildpack
```
heroku buildpacks:set heroku/python
```
Configure the environment variables (Heroku Config Vars)
```
heroku config:set TELEGRAM_TOKEN="{your Telegram token}"
heroku config:set MODE="webhook"
heroku config:set WEBHOOK_URL="https://advancedtelegrambot.herokuapp.com/"
```
### Deploy
```
git push heroku main
```



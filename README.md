# TelegramBotDemo
Simple Telegram Bot

Find here the source code of the [Advanced Telegram Chatbots: features that make a difference](https://towardsdatascience.com/bring-your-telegram-chatbot-to-the-next-level-c771ec7d31e4) 
article.

### Table of Contents 
  * [Setup](#setup)
  * [Run on Local](#run-on-local)
  * [Deploy to Heroku with Git](#deploy-to-heroku-with-git)
  * [Deploy to Heroku with Docker (on x86-64 architecture)](#deploy-to-heroku-with-docker--on-x86-64-architecture-)
  * [Deploy to Heroku with Docker (on ARM architecture)](#deploy-to-heroku-with-docker--on-arm-architecture-)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


##Setup

Clone the repository

```
git clone https://github.com/gcatanese/TelegramBotDemo.git
```

Create and *.env* file in the same folder as *app.py*. The *.env* file defines the environment variables.  

* TELEGRAM_TOKEN={your Telegram token} [here]


## Run on Local
Run the application
```
cd telegram_bot
python telegram_bot.py
```
Access the bot via the deeplink `https://t.me/{bot_username}` and start chatting

**Note**: the chatbot runs in Polling mode

## Deploy to Heroku with Git

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

## Deploy to Heroku with Docker (on x86-64 architecture)

When working on Intel64 architecture the Docker image can be built and pushed using the Heroku CLI.

### Prerequisites
* [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
* `Dockerfile` must be in the root folder
* Login into the Heroku Docker Registry: `heroku container:login`

### Create and Configure the Heroku app

Create a new app 
 
```
heroku create advancedtelegrambot
```

Configure the environment variables (Heroku Config Vars)
```
heroku config:set TELEGRAM_TOKEN="{your Telegram token}"
heroku config:set MODE="webhook"
heroku config:set WEBHOOK_URL="https://advancedtelegrambot.herokuapp.com/"
```
Build and push the image
```
heroku container:push web
```
Release the image
```
heroku container:release web
```

## Deploy to Heroku with Docker (on ARM architecture)

When working on ARM architecture the Docker image needs to be made compatible with Heroku x64, using the Docker 
command line together with the Buildx plugin.

### Prerequisites
* [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
* `Dockerfile` must be in the root folder
* Login into the Heroku Docker Registry: `heroku container:login`

### Create and Configure the Heroku app

Create a new app 
 
```
heroku create advancedtelegrambot
```

Configure the environment variables (Heroku Config Vars)
```
heroku config:set TELEGRAM_TOKEN="{your Telegram token}"
heroku config:set MODE="webhook"
heroku config:set WEBHOOK_URL="https://advancedtelegrambot.herokuapp.com/"
```
Build the image setting the `platform` used by Heroku
```
docker buildx build --platform linux/amd64 -t advancedtelegrambot .
```
Tag the image following Heroku naming conventions
```
docker tag advancedtelegrambot registry.heroku.com/advancedtelegrambot/web
```
Push the image into Docker Registry
```
docker push registry.heroku.com/advancedtelegrambot/web
```
Release the image
```
heroku container:release web -a advancedtelegrambot
```



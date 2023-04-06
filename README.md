# Data processing

## Configure OpenAI and Telegram api tokens

* Get token from Telegram - https://t.me/BotFather
* Get token from OpenAI - https://platform.openai.com/account/api-keys

## Configure environment variables

Create .env file under Cryptonews folder and copy all variables from .env.example
There is no TELEGRAM_CHAT_ID, to get it, run this script and copy it from console and fill .env

```shell
$ python3 data_processing/Posts/chatid.py
```

## Run project

```shell
$ python3 main.py
```
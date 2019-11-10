# Installation

If you are using gitpod that project gets automatically configured.

## For non-gitpod users:
1. The .env.example must by duplicated and renamed to `.env`, then replace variables with your own values.



# Runnin the application

WELCOME GEEK! 🐍 + 💻 = 🤓

The server is already running, `ctr + c` to stop the server if you like

The following commands are available to stat coding:

- pipenv run migrate create database migrations (if models.py is edited)
- pipenv run upgrade run database migrations (if pending)
- pipenv run start start flask web server (if not running)
- pipenv run diagram create database diagram image (if needed)
- pipenv run deploy deploy to heroku (if needed)
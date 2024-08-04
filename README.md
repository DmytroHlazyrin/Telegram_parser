# Telegram_parser

This project is designed to monitor Telegram messages and interact with them through a Telegram bot. 
The project consists of two main components: a script for parsing messages and a 
Telegram bot for displaying the latest messages.

## Table of Contents 📑

1. [Overview](#overview-)
2. [Features](#features-)
3. [Installation](#installation-)
4. [Setting up Environment Variables](#setting-up-environment-variables-)
5. [Starting the Project](#starting-the-project-)
6. [Run with Docker](#run-with-docker-)
7. [Getting Access](#getting-access-)


## Overview 🔎

This project is built using Python and the following technologies:
- [Telethon](https://github.com/LonamiWebs/Telethon): An asynchronous Python Telegram client library.
- [SQLAlchemy](https://www.sqlalchemy.org/): The Python SQL toolkit and Object-Relational Mapping (ORM) library.
- [Django](https://www.djangoproject.com/): A high-level Python web framework.
- [Docker](https://www.docker.com/): A platform for developing, shipping, and running applications in containers.

## Features

### Telegram Monitoring 📲

- Monitors Telegram messages from personal chats.
- Parses messages and stores them in a PostgreSQL database.

### Telegram Bot 🤖

- Displays the latest messages from the database.
- Provides a 'Show latest 10 messages' button.
- Loads more messages on demand.

## Installation 🔧

1. Clone the repository:

    ```shell
    git clone https://github.com/DmytroHlazyrin/Telegram_parser.git
    ```

2. Go to the project directory:

    ```shell
    cd Telegram_parser
    ```

3. Create and activate a virtual environment:

    ```shell
    python -m venv venv
    source venv/bin/activate  # On macOS or Linux
    venv\Scripts\activate  # On Windows
    ```

4. Install the required dependencies:

    ```shell
    pip install -r requirements.txt
    ```

## Setting up Environment Variables 🔐

1. Create a `.env` file in the project root directory:

    ```shell
    touch .env
    ```

2. Add the following environment variables to the `.env` file:

    ```env
    TELEGRAM_BOT_TOKEN=<your-telegram-bot-token>
    API_ID=<your-api-id>
    API_HASH=<your-api-hash>
    PHONE_NUMBER=<your-phone-number>
    DATABASE_URL=postgresql://<db_user>:<db_password>@<db_host>/<db_name>
    POSTGRES_USER=db_user
    POSTGRES_PASSWORD=db_user
    POSTGRES_DB=telegram_db
    ```

## Starting the Project 🚀

1. Creating the database tables and first parsing:

    ```shell
    python telethon_app.py
    ```

2. Start the Telegram bot:

    ```shell
    python telegram_bot.py
    ```

## Run with Docker 🐳

1. Build the Docker images and start the containers:

    ```shell
    docker-compose build
    docker-compose up
    ```
2. When you connect for the first time, you need to manually run the script 
to enter your phone number and then the secret code that will come to Telegram.
   The session data will be saved to the database.
   ```shell
    docker exec -it <container_name> /bin/sh
    python /app/telethon_app.py
    input(Enter your phone number:)
    input(Enter the secret code:)
    ```
The Docker Compose setup includes services for PostgreSQL, the Telegram bot, 
and the cron service for running the `telethon_app.py` script every 5 minutes.

## Getting Access 🔑

1. Create a Telegram bot and get the `TELEGRAM_BOT_TOKEN`. Follow the instructions from [Telegram's BotFather](https://core.telegram.org/bots#botfather).
2. Obtain your `API_ID` and `API_HASH` by following the instructions at [my.telegram.org](https://my.telegram.org/auth).

## Conclusion 🎉

Thank you for checking out the Telegram_parser project! I hope this solution helps you efficiently monitor and interact with your Telegram messages. If you have any questions or suggestions, feel free to reach out. Happy coding!

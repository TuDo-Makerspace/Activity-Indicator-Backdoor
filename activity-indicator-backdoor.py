#!/usr/bin/env python3

# Copyright (C) 2023 Patrick Pedersen, TUDO Makerspace

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Author: Patrick Pedersen <ctx.xda@gmail.com>

import argparse
import asyncio
import telegram
import logging
import configparser
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

POST_ENDPOINT = "/api/activityIndicator"

ai_bot = None
ai_chat_id = None
open_msg = None
close_msg = None
backdoor_chat_id = None

rest_uname = None
rest_pwd = None
rest_url = None


# Updates status on website via REST call
def send_post_request(open: bool):
    response = requests.post(
        rest_url + POST_ENDPOINT,
        data={"open": "true" if open else "false"},
        auth=(rest_uname, rest_pwd),
    )

    # Print error message if POST request failed
    if response.status_code != 200:
        print("activity-indicator-backdoor.py: Request Failed: " + response.text)


# Sends a message into the Activity Indicator broadcast channel
async def send_ai_message(message: str):
    await ai_bot.send_message(chat_id=ai_chat_id, text=message)


# Main handler for open/close requests
async def set_activity(update: Update, open: bool):
    if update.message.chat_id != backdoor_chat_id:
        await update.message.reply_text(
            "HALT! You are not authorized to use this command >:("
        )
        return
    await send_ai_message(open_msg if open else close_msg)
    send_post_request(open)
    await update.message.reply_text("The activity indicator has been updated!")


# /open command handler
async def open(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_activity(update, True)


# /close command handler
async def close(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_activity(update, False)


####################################################
# MAIN
####################################################


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Fallback Telegram bot to manually set the Activity Indicator"
    )
    parser.add_argument("--log_level", "-l", help="Log level", default="INFO")
    parser.add_argument(
        "--config_file", "-c", help="Config file", default="backdoor.ini"
    )

    args = parser.parse_args()

    # Start logging
    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Read config
    config = configparser.ConfigParser()
    config.read(args.config_file)

    backdoor_token = config["BackdoorBot"]["Token"]
    backdoor_chat_id = int(config["BackdoorBot"]["ChatID"])

    ai_bot = telegram.Bot(token=config["AIBot"]["Token"])

    ai_chat_id = int(config["AIBot"]["ChatID"])
    open_msg = config["AIBot"]["OpenMessage"]
    close_msg = config["AIBot"]["CloseMessage"]

    rest_uname = config["Website"]["Username"]
    rest_pwd = config["Website"]["Password"]
    rest_url = config["Website"]["URL"]

    # Set up command handlers
    app = ApplicationBuilder().token(backdoor_token).build()
    open_handler = CommandHandler("open", open)
    close_handler = CommandHandler("close", close)
    app.add_handler(open_handler)
    app.add_handler(close_handler)

    # Run server
    app.run_polling()

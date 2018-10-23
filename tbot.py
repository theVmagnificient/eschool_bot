#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler, RegexHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup

import logging
import constants
from util_func import *

from req import *
from db import *
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)



def main():
    """Start"""
    DBInstance.init()

    updater = Updater(constants.token)
    dp = updater.dispatcher
    j = updater.job_queue
    j.run_repeating(callback_minute, interval=60, first=0)


    #Sign In
    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            LOG: [MessageHandler(Filters.text, Login)],

            PAS: [MessageHandler(Filters.text, Password)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    #Main functions
    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler('marks', Marks)],

        states={
            MARK1: [MessageHandler(Filters.text, Marks1)],

            MARK2: [MessageHandler(Filters.text, Marks2)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    #dialog messengs
    dp.add_handler(conv_handler1)
    dp.add_handler(conv_handler2)

    dp.add_handler(CommandHandler("help", help))
    #Hiden commands
    dp.add_handler(CommandHandler('info', info))

    dp.add_handler(CommandHandler('who_is_loh', Kirill))
    dp.add_handler(CommandHandler('kto_loh', Kirill))
    dp.add_handler(CommandHandler('top_tester', Denis))

    #updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo_msg))
    dp.add_handler(MessageHandler(Filters.command, echo_cmd))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

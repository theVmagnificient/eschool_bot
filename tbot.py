#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import logging
import constants
from req import *
from db import *
from tbot_functions import *
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

a = EschoolConnectionHandler()


LOG, PAS, AUT1, AUT2, AUT3 = range(5)
login, pas = [], []
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    #use this command or 'update.message.reply_text(str)'
    #bot.send_message(chat_id=update.message.chat_id, text="Привет☺☺☺        Я - бот для удобного использования сервиса eSchool    "
    #                                                      "электронного дневника для зоки.          "
    #                                                      "Для начала работы мне понадобится твой Логин и Пароль:")
    DBInstance.init()
    DBInstance.push(update.message.chat_id, '', '', 0)
    print('Yeah')
    update.message.reply_text('Привет☺☺☺')
    update.message.reply_text("Я - бот для удобного использования сервиса eSchool - электронного дневника для зоки.")
    update.message.reply_text("Для начала работы мне понадобится твой Логин и Пароль:")
    update.message.reply_text('Логин:')
    return LOG
def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Бог тебе в помощь')

def echo_msg(bot, update):
    """Echo the user message."""
    update.message.reply_text('Я ещё не научился распознавать это сообщение(')

def echo_cmd(bot, update):
    """Echo the user message."""
    update.message.reply_text('Я ещё не научился распознавать эту команду(')

def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
#Text functions:
def Kirill(bot, update):
    update.message.reply_text('Кирилл Лопатин лох, очевидно.')

def Login(bot, update):
    update.message.reply_text('Пароль:')
    DBInstance.update(update.message.chat_id,update.message.text, '')
    return PAS

def Password(bot, update):
    pas = update.message.text
    DBInstance.update(update.message.chat_id, '', pas)
    if a.login(DBInstance.get(update.message.chat_id).login, DBInstance.get(update.message.chat_id).password) != 0:
        DBInstance.delete(update.message.chat_id)
        update.message.reply_text('Неправильный логин или пароль, попробуй ещё раз:')
        update.message.reply_text('Логин:')
        return LOG
    else:
        update.message.reply_text('Ура, всё залогинилось!')
        update.message.reply_text('Напиши любое сообщение для продолжения...')
        return AUT1

def Aut1(bot, update):
    keyboard = [[InlineKeyboardButton("Оценки за 1 полугодие", callback_data='1 полугодие'),
                 InlineKeyboardButton("Оценки за 2 полугодие", callback_data='2 полугодие')],
                [InlineKeyboardButton("Оценки за 2 полугодие", callback_data='1 четверть'),
                 InlineKeyboardButton("Оценки за 2 полугодие", callback_data='2 четверть')],


                [InlineKeyboardButton("За год", callback_data='год')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Выбери промежуток:', reply_markup=reply_markup)
    return ConversationHandler.END
    return AUT2

def Aut2(bot, update):
    query = update.callback_query

    print(a.get_user_id())

    print(a.get_avg_mark(per_name=query.data))
    #bot.edit_message_text(text="Selected option: {}".format(query.data),
    #                      chat_id=query.message.chat_id,
    #                      message_id=query.message.message_id)

    return AUT3

def Aut3(bot, update):

    return ConversationHandler.END
#end of text functions

def main():
    """Start"""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(constants.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            LOG: [MessageHandler(Filters.text, Login)],

            PAS: [MessageHandler(Filters.text, Password)],

            AUT1: [MessageHandler(Filters.text, Aut1)],

            AUT2: [MessageHandler(Filters.text, Aut2)],

            AUT3: [MessageHandler(Filters.text, Aut3)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    #log = input("Log: ")
    #pas = input("Pas: ")
    #a.login(log, pas)
    #print(a.get_user_id())

    # on different commands - answer in Telegram
    dp.add_handler(conv_handler)
    #dp.add_handler(CommandHandler("help", help))
    #dp.add_handler(CommandHandler('who_is_loh', Kirill))
    #updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo_msg))
    #dp.add_handler(MessageHandler(Filters.command, echo_cmd))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler, RegexHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup
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
my_bot = Bot()

#define main states
LOG, PAS, MARK1, MARK2, MARK3 = range(5)

def echo_msg(bot, update):
    """Echo the user message."""
    update.message.reply_text('Я ещё не научился распознавать это сообщение(')

def echo_cmd(bot, update):
    """Echo the user message."""
    update.message.reply_text('Я ещё не научился распознавать эту команду(')

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Окей...\nНапиши, когда будет время :(.',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Бог тебе в помощь')

#Text functions:
def Kirill(bot, update):
    update.message.reply_text('Кирилл Лопатин лох, очевидно.')

""" Authentication branch """
def start(bot, update):
    """Send a message when the command /start is issued."""
    #use this command or 'update.message.reply_text(str)'
    #bot.send_message(chat_id=update.message.chat_id, text="Привет☺☺☺        Я - бот для удобного использования сервиса eSchool    "
    #                                                      "электронного дневника для зоки.          "
    #                                                      "Для начала работы мне понадобится твой Логин и Пароль:")
    DBInstance.init()
    DBInstance.push(update.message.chat_id, '', '', 0)
    print('Yeah')

    update.message.reply_text('Привет☺☺☺\nЯ - бот для удобного использования сервиса eSchool - электронного дневника для зоки.\n'
                              'Для начала работы мне понадобится твой Логин и Пароль:\n')
    update.message.reply_text('Логин:')
    return LOG

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
        update.message.reply_text('Теперь тебе доступны все команды!\n Используй /help для просмотра списка команд.')
        my_bot.IsLog = True
        return ConversationHandler.END

""" Main functional branch """
def Marks(bot, update):
    if my_bot.IsLog == False:
        update.message.reply_text('Ой, ты ещё не авторизовался в систему.\nПопробуй /start')
        return ConversationHandler.END

    reply_keyboard = [['1 четверть', '2 четверть', '3 четверть', '4 четверть'],
                      ['1 полугодие', '2 полугодие'],
                      ['год']
                     ]
    update.message.reply_text(
        'Выбери период, за который ты хочешь узнать средний балл',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
    return MARK1

def Marks1(bot, update):
    my_bot.currentPeriod = update.message.text

    #per_name=text
    #update.message.reply_text(a.get_avg_mark(per_name=text))
    reply_keyboard = [
        ['Алгебра', 'Английский язык', 'Биология'],
        ['География', 'Геометрия', 'Информатика и ИКТ'],
        ['Искусство', 'История', 'Литература'],
        ['Обществознание', 'Русский язык', 'Физика'],
        ['Физическая культура', 'Химия', 'Урок классного руководителя']
    ]
    update.message.reply_text(
        'И введи предмет:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
    return MARK2

def Marks2(bot, update):
    my_bot.currentSubject = update.message.text
    update.message.reply_text('Твой стредний балл по {} за {}:'.format(my_bot.currentSubject, my_bot.currentPeriod))
    update.message.reply_text(a.get_avg_mark(subj_name=my_bot.currentSubject, per_name=my_bot.currentPeriod))
    return ConversationHandler.END
#end of text functions

def main():
    """Start"""
    updater = Updater(constants.token)
    dp = updater.dispatcher

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
    # on different commands - answer in Telegram
    dp.add_handler(conv_handler1)
    dp.add_handler(conv_handler2)
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('who_is_loh', Kirill))
    #updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo_msg))
    #dp.add_handler(MessageHandler(Filters.command, echo_cmd))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

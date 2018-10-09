#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler, RegexHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup
import logging
import constants
from tbot_classes import *
from req import *
from db import *
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

my_bot = Bot()

#define main states
LOG, PAS, MARK1, MARK2, MARK3 = range(5)

def echo_msg(bot, update):
    """Echo the user message."""
    user = update.message.from_user
    update.message.reply_text('Я ещё не научился распознавать это сообщение(')
    my_bot.echomsg += [user.full_name + ':', update.message.text]

def echo_cmd(bot, update):
    user = update.message.from_user
    update.message.reply_text('Я ещё не научился распознавать эту команду(')
    my_bot.echocmd += [user.full_name + ':', update.message.text]

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Окей...\nНапиши, когда будет время :(.',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
def help(bot, update):
    update.message.reply_text('Вот список некоторых команд:\n/start - Для старта и авторизации\n/help - ага\n/marks - Узнать средний балл\n\n'
                              'Спасибо, что используете нашего бота!\n'
                              'Если у вас есть вопросы, предложения,\n или вы просто хотите сказать какие мы классные\n'
                              'То пишите в телеграм - +79110345864,\n'
                              'или найдите другой способ связаться со мной. 10-5 Степан 2018')

#Text functions:

#Secret commands
def info(bot, update):
    if my_bot.get_user(update.message.chat_id).IsAdmin == 1:
        update.message.reply_text('Messages from users:')
        for i in my_bot.echomsg:
            update.message.reply_text(str(i))
        update.message.reply_text('Commands from users:')
        for i in my_bot.echocmd:
            update.message.reply_text(str(i))
        update.message.reply_text('Number of users in this session:')
        update.message.reply_text(str(my_bot.numberofUsers))
    else:
        update.message.reply_text('Я ещё не научился распознавать эту команду(')

def Kirill(bot, update):
    update.message.reply_text('Кирилл Лопатин лох, очевидно.')

def Denis(bot, update):
    update.message.reply_text('Денис тарасов бог, roflanebalo')

""" Authentication branch """
def start(bot, update):
    """Send a message when the command /start is issued."""
    l = DBInstance.get(update.message.chat_id)

    my_bot.new_user(update.message.chat_id)

    if l != "User doesn't exist":
        if my_bot.get_user(update.message.chat_id).ES.login(DBInstance.get(update.message.chat_id).login,
                                                        DBInstance.get(update.message.chat_id).password, ishash_pas=True) == 0:
            print(DBInstance.get(update.message.chat_id).login, DBInstance.get(update.message.chat_id).password)
            if DBInstance.get(update.message.chat_id).login == 'Sinyakov':
                my_bot.get_user(update.message.chat_id).IsAdmin = True
            update.message.reply_text('Я нашёл данные твоего аккаунта в нашей базе данных,\n и сразу авторизовался.')
            update.message.reply_text('Теперь тебе доступны все команды!\n Используй /help для просмотра списка команд.')
            my_bot.get_user(update.message.chat_id).currentClass = my_bot.get_user(update.message.chat_id).ES.get_user_grade()
            my_bot.get_user(update.message.chat_id).Islog = True
            return ConversationHandler.END

    DBInstance.push(update.message.chat_id, '', '', 0)
    update.message.reply_text('Привет! ☻☻☻\n'
                              'Я - один из самых классных ботов в телеграме,\n'
                              'и я создан цгшниками из ГФМЛ №30\n'
                              'А именно: KL1 и SS5(CGSG FOREVER).\n'
                              'Я предназначен для комфортного использования\n сервиса eSchool - \n\n'
                              )
    update.message.reply_html('https://app.eschool.center/#/Main')
    update.message.reply_text('Для начала работы мне понадобится твой Логин и Пароль:\n')
    update.message.reply_text('Логин:')
    return LOG

def Login(bot, update):
    update.message.reply_text('Пароль:')
    my_bot.get_user(update.message.chat_id).sLogin = update.message.text
    DBInstance.update(update.message.chat_id,update.message.text, '')
    return PAS

def Password(bot, update):
    pas = update.message.text
    DBInstance.update(update.message.chat_id, '', pas)
    my_bot.get_user(update.message.chat_id).sPassword = pas
    l = DBInstance.get(update.message.chat_id)
    #if l == "User doesn't exist":
    #    update.message.reply_text('Неправильный логин или пароль, попробуй ещё раз:')
    #    update.message.reply_text('Логин:')
    #    return LOG

    #if my_bot.get_user(update.message.chat_id).login(
    #        DBInstance.get(update.message.chat_id).login,DBInstance.get(update.message.chat_id).password) != 0:
    #    DBInstance.delete(update.message.chat_id)
    #    update.message.reply_text('Неправильный логин или пароль, попробуй ещё раз:')
    #    update.message.reply_text('Логин:')
    #    return LOG
    if my_bot.get_user(update.message.chat_id).login(
            my_bot.get_user(update.message.chat_id).sLogin,my_bot.get_user(update.message.chat_id).sPassword) != 0:
        DBInstance.delete(update.message.chat_id)
        update.message.reply_text('Неправильный логин или пароль, попробуй ещё раз:')
        update.message.reply_text('Логин:')
        return LOG
    else:
        DBInstance.update(update.message.chat_id, '', my_bot.get_user(update.message.chat_id).ES.hash_pas)
        update.message.reply_text('Ура, всё залогинилось!')
        update.message.reply_text('Теперь тебе доступны все команды!\n Используй /help для просмотра списка команд.')
        my_bot.get_user(update.message.chat_id).Islog = True
        my_bot.numberofUsers += 1
        #if DBInstance.get(update.message.chat_id).login == 'Sinyakov':
        #    my_bot.get_user(update.message.chat_id).IsAdmin = True
        return ConversationHandler.END

""" Main functional branch """
def Marks(bot, update):
    if my_bot.get_user(update.message.chat_id).Islog == False:
        update.message.reply_text('Ой, ты ещё не авторизовался в систему.\nПопробуй /start')
        return ConversationHandler.END

    if my_bot.get_user(update.message.chat_id).ES.get_user_grade() == '5-9 кл':
        reply_keyboard = my_bot.nineClPeriods
    elif my_bot.get_user(update.message.chat_id).ES.get_user_grade()  == '10 кл' or\
            my_bot.get_user(update.message.chat_id).ES.get_user_grade()  == '11 кл':
        reply_keyboard = my_bot.tenClPeriods

    update.message.reply_text(
        'Выбери период, за который ты хочешь узнать средний балл',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
    return MARK1

def Marks1(bot, update):
    my_bot.get_user(update.message.chat_id).currentPeriod = update.message.text
    if my_bot.get_user(update.message.chat_id).ES.get_user_grade()  == '5-9 кл':
        keyboard = my_bot.nineClMenu
    elif my_bot.get_user(update.message.chat_id).ES.get_user_grade()  == '10 кл' or \
            my_bot.get_user(update.message.chat_id).ES.get_user_grade()  == '11 кл':
        keyboard = my_bot.tenClMenu
    #per_name=text
    #update.message.reply_text(a.get_avg_mark(per_name=text))
    update.message.reply_text(
        'И введи предмет:',
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))
    return MARK2

def Marks2(bot, update):
    my_bot.get_user(update.message.chat_id).currentSubject = update.message.text

    mark = my_bot.get_user(update.message.chat_id).ES.get_avg_mark(subj_name=my_bot.get_user(update.message.chat_id).currentSubject,
                                                                                      per_name=my_bot.get_user(update.message.chat_id).currentPeriod)
    #if mark == '0.0':
    #    update.message.reply_text('У тебя ещё нет оценок по этому предмету!')
    #else:
    update.message.reply_text(
        'Твой стредний балл по {} за {}:'.format(my_bot.get_user(update.message.chat_id).currentSubject,
                                                 my_bot.get_user(update.message.chat_id).currentPeriod))
    update.message.reply_text(mark)
    return ConversationHandler.END
#end of text functions

def main():
    """Start"""
    DBInstance.init()

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

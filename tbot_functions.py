#from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ReplyKeyboardMarkup

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

    """
    #variant 1
    button_list = [
        InlineKeyboardButton("col1", callback_data='1'),
        InlineKeyboardButton("col2", callback_data='2'),
        InlineKeyboardButton("row 2", callback_data='3')
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    """
    #variant 2
    """ REALISE
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    """
class Bot:
    def __init__(self):
        self.IsLog = False
        self.currentPeriod = None
        self.currentSubject = None
    def push_is_Log(self):
        self.IsLog = True

    def get_is_Log(self):
        return self.IsLog

def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

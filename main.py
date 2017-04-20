"""
Simple python bot file for logging message.
You need python-telegram-bot module.
Use 'pip install -U python-telegram-bot' for install module.
"""
import logging
import time
import os.path

import token_value

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

UPDATER = Updater(token=token_value.KEY)
DISPATCHER = UPDATER.dispatcher

#Alarm format text
ALARM_WRONG_FORMAT = 'Input wrong format\nExample : /import YYYY/MM/DD'
ALARM_WRONG_PATH = 'Log on input date is not exist'

logging.basicConfig(format='%(message)s', level=logging.INFO)

def import_log(bot, update, args):
    """
    Import log file by user input
    """
    #If argument not exist, send alarm message to user.
    if not args:
        bot.sendMessage(chat_id=update.message.chat_id, text=ALARM_WRONG_FORMAT)
        return

    #Split args into new list, which contain year, month and day value
    new_arg = args[0].split('/')
    (year, month, day) = (str(new_arg[0]), str(new_arg[1]), str(new_arg[2]))

    #If input value is not numeric, send alarm message to user.
    if len(new_arg) < 3 or not year.isalnum() or not month.isalnum() or not day.isalnum():
        bot.sendMessage(chat_id=update.message.chat_id, text=ALARM_WRONG_FORMAT)
        return

    #set file path as './log/YYYY/MM/YYYY-MM-DD.log'
    #You may change if you want, but you have to change other path too.
    filepath = './log/' + year + '/' + month + '/' + year + '-' + month + '-' + day + '.log'

    #If path not exist, that mean there is no log with input format, so send alarm message to user.
    if not os.path.isfile(filepath):
        bot.sendMessage(chat_id=update.message.chat_id, text=ALARM_WRONG_PATH)
        return
    
    #Send log file to user.
    bot.sendDocument(chat_id=update.message.chat_id, document=open(filepath, 'rb'))

def save_text_log(bot, update):
    """
    Save log with timeline and user_name
    """
    #set directory path './log/YYYY/MM/'
    #You may change if you want, but you have to change other path too.
    dir_path = './log/' + time.strftime('%Y/%m/')

    #If directory not exist, create new directory
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    #set log file path as './log/YYYY/MM/YYYY-MM-DD.log'
    #You may change if you want, but you have to change other path too.
    logname = dir_path + time.strftime('%Y-%m-%d') + '.log'

    #Create logger and add to handler
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(logname)
    logger.addHandler(file_handler)

    #Log text format as '[YYYY-MM-DD HH:MM:SS] "User name" : "User message"'
    #You may change if you want
    log_text = "[" + time.strftime('%Y-%m-%d %H:%M:%S') + "] " + update.message.from_user.first_name + " : " + update.message.text
    logging.info(log_text)

    #Remove handler because it will keep remaining
    logger.removeHandler(file_handler)

def save_photo_log(bot, update):
    """
    Save log with timeline and user_name on command
    """
    #set directory path as './pic/YYYY/MM/DD/'
    #You may change if you want
    dir_path = './pic/' + time.strftime('%Y/%m/%d/')

    #If directory not exist, create new directory
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    #set photo file path as './pic/YYYY/MM/DD/YYYY-MM-DD HH-MM-SS.jpg'
    #You may change if you want, but you have to change other path too.
    filepath = dir_path + time.strftime('%Y-%m-%d %H-%M-%S') + '.jpg'

    #Get largest photo file and download it.
    get_file = bot.getFile(update.message.photo[len(update.message.photo)-1].file_id)
    get_file.download(custom_path=filepath)

def __main__():
    import_handler = CommandHandler('import', import_log, pass_args=True)
    #Logging text not only text but also command.
    text_log_handler = MessageHandler(Filters.text | Filters.command, save_text_log)
    photo_log_handler = MessageHandler(Filters.photo, save_photo_log)

    #You must put import_handler first, for preventing collision with text_log_handler which correct command.
    DISPATCHER.add_handler(import_handler)
    DISPATCHER.add_handler(text_log_handler)
    DISPATCHER.add_handler(photo_log_handler)

    UPDATER.start_polling()
    UPDATER.idle()

if __name__ == '__main__':
    __main__()

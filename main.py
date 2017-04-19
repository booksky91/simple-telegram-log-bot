"""
Bot file for test python
"""
import logging
import time
import os.path
import token
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

UPDATER = Updater(token=token.value)
DISPATCHER = UPDATER.dispatcher

ALARM_WRONG_FORMAT = '잘못된 값을 넣었습니다.\n올바른 형식 : /import YYYY/MM/DD'
ALARM_WRONG_PATH = '해당 날짜의 로그는 존재하지 않습니다.'

logging.basicConfig(format='%(message)s', level=logging.INFO)

def import_log(bot, update, args):
    """
    import log file from server
    """
    print(args)
    new_arg = args[0].split('/')

    if args == None or len(new_arg) < 3:
        bot.sendMessage(chat_id=update.message.chat_id, text=ALARM_WRONG_FORMAT)
        return
    elif not new_arg[0].isalnum() or not new_arg[1].isalnum() or not new_arg[2].isalnum():
        bot.sendMessage(chat_id=update.message.chat_id, text=ALARM_WRONG_FORMAT)
        return

    filename = './log/' + str(new_arg[0]) + '-' + str(new_arg[1]) + '-' + str(new_arg[2]) + '.log'
    if not os.path.isfile(filename):
        bot.sendMessage(chat_id=update.message.chat_id, text=ALARM_WRONG_PATH)
        return

    readfile = open(filename, 'rb')
    bot.sendDocument(chat_id=update.message.chat_id, document=readfile)

def save_log(bot, update):
    """
    Save log with timeline and user_name
    """
    logname = './log/' + time.strftime('%Y-%m-%d') + '.log'

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(logname)
    logger.addHandler(file_handler)

    log_text = "[" + time.strftime('%Y-%m-%d %H:%M:%S') + "] " + update.message.from_user.first_name + " : " + update.message.text
    logging.info(log_text)
    logger.removeHandler(file_handler)

def __main__():
    import_handler = CommandHandler('import', import_log, pass_args=True)
    log_handler = MessageHandler(Filters.text, save_log)

    DISPATCHER.add_handler(import_handler)
    DISPATCHER.add_handler(log_handler)

    UPDATER.start_polling()
    UPDATER.idle()

if __name__ == '__main__':
    __main__()

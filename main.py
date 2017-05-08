"""
Bot file for test python
"""
import logging
import time
import os.path

import token_value

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

UPDATER = Updater(token=token_value.KEY)
DISPATCHER = UPDATER.dispatcher

ALARM_WRONG_FORMAT = '잘못된 값을 넣었습니다.\n올바른 형식 : /import YYYY/MM/DD'
ALARM_WRONG_PATH = '해당 날짜의 로그는 존재하지 않습니다.'

logging.basicConfig(format='%(message)s', level=logging.INFO)

def import_log(bot, update, args):
    """
    import log file from server
    """

    if not args:
        filename = './log/' + time.strftime('%Y/%m/%Y-%m-%d') + '.log'
    else:
        new_arg = args[0].split('/')

        if len(new_arg) < 3 or not str(new_arg[0]).isalnum() or not str(new_arg[1]).isalnum() or not str(new_arg[2]).isalnum():
            bot.sendMessage(chat_id=update.message.chat_id, text=ALARM_WRONG_FORMAT)
            return

        filename = './log/' + str(new_arg[0]) + '/' + str(new_arg[1]) + '/' + str(new_arg[0]) + '-' + str(new_arg[1]) + '-' + str(new_arg[2]) + '.log'

    if not os.path.isfile(filename):
        bot.sendMessage(chat_id=update.message.chat_id, text=ALARM_WRONG_PATH)
        return

    bot.sendDocument(chat_id=update.message.chat_id, document=open(filename, 'rb'))

def save_text_log(bot, update):
    """
    Save log with timeline and user_name on text
    """
    dir_path = './log/' + time.strftime('%Y/%m/')

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    logpath = dir_path + time.strftime('%Y-%m-%d') + '.log'

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(logpath)
    logger.addHandler(file_handler)

    log_text = "[" + time.strftime('%Y-%m-%d %H:%M:%S') + "] " + update.message.from_user.first_name + " : " + update.message.text
    logging.info(log_text)
    logger.removeHandler(file_handler)

def save_photo_log(bot, update):
    """
    Save log with timeline and user_name on photo
    """
    dir_log_path = './log/' + time.strftime('%Y/%m/')
    dir_pic_path = './pic/' + time.strftime('%Y/%m/%d/')

    if not os.path.exists(dir_log_path):
        os.makedirs(dir_log_path)

    if not os.path.exists(dir_pic_path):
        os.makedirs(dir_pic_path)

    logpath = dir_log_path + time.strftime('%Y-%m-%d') + '.log'

    if not update.message.photo:
        pic_file_id = update.message.sticker.thumb.file_id
    else:
        pic_file_id = update.message.photo[len(update.message.photo)-1].file_id
        filepath = dir_pic_path + time.strftime('%Y-%m-%d %H-%M-%S ') + pic_file_id + '.jpg'
        get_file = bot.getFile(pic_file_id)
        get_file.download(custom_path=filepath)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(logpath)
    logger.addHandler(file_handler)

    log_text = "[" + time.strftime('%Y-%m-%d %H:%M:%S') + "] " + update.message.from_user.first_name + " : " + pic_file_id
    logging.info(log_text)
    logger.removeHandler(file_handler)

def __main__():
    import_handler = CommandHandler('import', import_log, pass_args=True)
    text_log_handler = MessageHandler(Filters.text | Filters.command | Filters.reply, save_text_log, message_updates=True)
    photo_log_handler = MessageHandler(Filters.photo | Filters.sticker, save_photo_log)

    DISPATCHER.add_handler(import_handler)
    DISPATCHER.add_handler(text_log_handler)
    DISPATCHER.add_handler(photo_log_handler)

    UPDATER.start_polling()
    UPDATER.idle()

if __name__ == '__main__':
    __main__()

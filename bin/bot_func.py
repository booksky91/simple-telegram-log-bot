"""
Function for log bot file
"""
import time
import os.path
import logging

import bot_setting

logging.basicConfig(format='%(message)s', level=logging.INFO)

def import_log(bot, update, args):
    """
    import log file from server
    """

    if not args:
        filename = bot_setting.DEFAULT_PATH + 'log/text/' + time.strftime('%Y/%m/%Y-%m-%d') + '.log'
    else:
        new_arg = args[0].split('/')

        if len(new_arg) < 3 or not str(new_arg[0]).isalnum() or not str(new_arg[1]).isalnum() or not str(new_arg[2]).isalnum():
            bot.sendMessage(chat_id=update.message.chat_id, text=bot_setting.ALARM_WRONG_FORMAT)
            return

        filename = './log/' + str(new_arg[0]) + '/' + str(new_arg[1]) + '/' + str(new_arg[0]) + '-' + str(new_arg[1]) + '-' + str(new_arg[2]) + '.log'

    if not os.path.isfile(filename):
        bot.sendMessage(chat_id=update.message.chat_id, text=bot_setting.ALARM_WRONG_PATH)
        return

    bot.sendDocument(chat_id=update.message.chat_id, document=open(filename, 'rb'))

def save_text_log(bot, update):
    """
    Save log with timeline and user_name on text
    """
    dir_path = bot_setting.DEFAULT_PATH + 'log/text/' + time.strftime('%Y/%m/')

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
    dir_log_path = bot_setting.DEFAULT_PATH + 'log/text/' + time.strftime('%Y/%m/')
    dir_pic_path = bot_setting.DEFAULT_PATH + 'log/pic/' + time.strftime('%Y/%m/%d/')

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

"""
Bot file for test python
"""
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import bot_setting
import bot_func

UPDATER = Updater(token=bot_setting.KEY)
DISPATCHER = UPDATER.dispatcher

def __main__():
    import_handler = CommandHandler('import', bot_func.import_log, pass_args=True)
    text_log_handler = MessageHandler(Filters.text | Filters.command | Filters.reply, bot_func.save_text_log)
    photo_log_handler = MessageHandler(Filters.photo | Filters.sticker, bot_func.save_photo_log)

    DISPATCHER.add_handler(import_handler)
    DISPATCHER.add_handler(text_log_handler)
    DISPATCHER.add_handler(photo_log_handler)

    UPDATER.start_polling()
    UPDATER.idle()

if __name__ == '__main__':
    __main__()

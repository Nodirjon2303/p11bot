from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler, CallbackContext, \
    ConversationHandler

import logging
from functions import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', start)
    ],
    states={
        'state_name': [
            CommandHandler('start', start),
            MessageHandler(Filters.text, command_name)
        ],
        'state_phone': [
            MessageHandler(Filters.text, command_phone),
            MessageHandler(Filters.contact, command_phone)
        ],
        'state_viloyat': [
            CommandHandler('start', start),
            MessageHandler(Filters.text, command_viloyat)
        ],
        'state_main': [
            CallbackQueryHandler(command_category)
        ],
        'state_product': [
            CallbackQueryHandler(command_product)
        ],
        'state_product_quantity': [
            CallbackQueryHandler(command_product_quantity)
        ],
        'state_savatcha': [
            CallbackQueryHandler(command_savatcha)
        ],
        'state_location':[
            MessageHandler(Filters.location, callback=command_location)
        ],
        'state_check_location':[
            MessageHandler(Filters.location, callback=command_location),
            MessageHandler(Filters.regex('^(' + 'Tasdiqlash' + ')$'), callback=command_confirm)
        ]
    },
    fallbacks=[
        CommandHandler('start', start)
    ]
)
updater = Updater("5310535030:AAEmVtjN_Gwr_UNxrVV6zF0tYzYttvX-LO0")
updater.dispatcher.add_handler(conv_handler)
updater.start_polling()
updater.idle()

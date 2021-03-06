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
        'state_location': [
            MessageHandler(Filters.location, callback=command_location)
        ],
        'state_check_location': [
            MessageHandler(Filters.location, callback=command_location),
            MessageHandler(Filters.regex('^(' + 'Tasdiqlash' + ')$'), callback=command_confirm)
        ],
        'state_history': [
            CallbackQueryHandler(command_history)
        ],
        'state_admin': [
            MessageHandler(Filters.regex('^(' + 'Statistika' + ')$'), callback=command_statistika),
            MessageHandler(Filters.regex('^(' + 'Reklama' + ')$'), callback=command_admin_reklama),
            MessageHandler(Filters.text, command_admin_main)
        ],
        'state_add_category': [
            CommandHandler('start', start),
            MessageHandler(Filters.text, command_add_category)
        ],
        'state_add_product_category': [
            CallbackQueryHandler(command_add_product_category)
        ],
        'state_add_product_name': [
            CommandHandler('start', start),
            MessageHandler(Filters.text, command_add_product_name)
        ],
        'state_add_product_price': [
            CommandHandler('start', start),
            MessageHandler(Filters.text, command_add_product_price)
        ],
        'state_add_product_image': [
            MessageHandler(Filters.photo, command_add_product_photo)
        ],
        'join_confirm': [
            CallbackQueryHandler(command_join_confirm)
        ],
        'state_reklama': [
            MessageHandler(Filters.all, command_send_reklama)
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

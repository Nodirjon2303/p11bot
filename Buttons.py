
from telegram import  ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from database import *

def phone_button():
    button = [
        [KeyboardButton('raqamni yuborish', request_contact=True)]
    ]
    return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)


def main_button():
    data = get_all_categories()
    button = []
    res = []
    for i in data:
        res.append(InlineKeyboardButton(i[1], callback_data=i[0]))
        if len(res) == 2:
            button.append(res)
            res = []

    if len(res)>0:
        button.append(res)
        
    button.append([InlineKeyboardButton("Buyurtmalar tarixi", callback_data='history')])
    button.append([InlineKeyboardButton("Savatchaga o'tish", callback_data='savatcha')])

    return InlineKeyboardMarkup(button)


def product_button_bycat(cat_id):
    products = get_products_by_catid(cat_id)
    button = []
    res = []
    for i in products:
        res.append(InlineKeyboardButton(i[2], callback_data=i[0]))
        if len(res) == 2:
            button.append(res)
            res = []
    if len(res)>0:
        button.append(res)
    button.append([InlineKeyboardButton('Orqaga', callback_data='back')])

    return InlineKeyboardMarkup(button)
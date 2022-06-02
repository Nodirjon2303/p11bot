
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


def quantity_button(soni = '0'):
    button = []
    res = []
    button.append([InlineKeyboardButton(f'Tanlangan: {soni}', callback_data='quantity')])
    for i in range(1, 10):
        res.append(InlineKeyboardButton(f"{i}", callback_data=f'{i}'))
        if len(res)==3:
            button.append(res)
            res = []
    res.append(InlineKeyboardButton('0', callback_data='0'))
    res.append(InlineKeyboardButton('O\'chirish', callback_data='delete'))
    button.append(res)
    button.append([InlineKeyboardButton('Savatchaga joylash', callback_data='savat')])
    button.append([InlineKeyboardButton('Orqaga', callback_data='back')])

    return InlineKeyboardMarkup(button)
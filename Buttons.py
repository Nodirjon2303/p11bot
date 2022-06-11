
from telegram import  ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from database import *

def phone_button():
    button = [
        [KeyboardButton('raqamni yuborish', request_contact=True)]
    ]
    return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)

def location_button():
    button = [
        [KeyboardButton('Manzilni yuborish', request_location=True)]
    ]
    return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)


def check_location_button():
    button = [
        ['Tasdiqlash', KeyboardButton('Manzilni qayta  yuborish', request_location=True)]
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

def category_button():
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



def savatcha_button(order_details):
    button = []
    res = []
    for i in order_details:
        product = get_product(i[2])
        res.append(InlineKeyboardButton("➕", callback_data=f'plus_{i[0]}'))
        res.append(InlineKeyboardButton(f"{product[2]}", callback_data=f'product'))
        res.append(InlineKeyboardButton("➖", callback_data=f'minus_{i[0]}'))
        button.append(res)
        res = []
    button.append([InlineKeyboardButton("Buyurtmani tasdiqlash", callback_data='confirm')])
    button.append([InlineKeyboardButton("Yana buyurtma berish", callback_data='again')])
    return InlineKeyboardMarkup(button)

def history_button(sahifa, jami):
    button  = [
        [InlineKeyboardButton(f'📖 Sahifa {sahifa}/{jami}', callback_data=f"{sahifa}")],
        [InlineKeyboardButton(f"⬅️Orqaga",callback_data='back')]
    ]
    return InlineKeyboardMarkup(button)

def admin_main_button():
    button = [
        ['Kategoriya qo\'shish'],
        ['Mahsulot qo\'shish']
    ]
    return ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)


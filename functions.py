from telegram import Update
from telegram.ext import CallbackContext
from Buttons import *
from database import *


def start(update: Update, context: CallbackContext):
    print("Assalomu alaykum")
    if check_user(update.effective_user.id):
        update.message.reply_text("Assalomu alaykum", reply_markup=ReplyKeyboardRemove())
        update.message.reply_text("Buyurtmani birga joylashtiramizmi? 🤗", reply_markup=main_button())
        return 'state_main'
    update.message.reply_text("Assalomu alaykum Botimizga xush kelibsiz\n"
                              "Ro'yxatdan o'tish uchun FIO ni yuboring", reply_markup=ReplyKeyboardRemove())
    return 'state_name'


def command_name(update: Update, context: CallbackContext):
    text = update.message.text
    update.message.reply_text("Sizning ismi familyangiz " + text + "\n"
                                                                   "Yaxshi endi telefon raqamingizni yuboring",
                              reply_markup=phone_button())
    context.user_data['name'] = text
    return 'state_phone'


def command_phone(update: Update, context: CallbackContext):
    try:
        contact = update.message.contact
        phone_number = contact.phone_number
    except Exception as e:
        phone = update.message.text
        if (phone[0] == '+' and len(phone) == 13 and phone[1:4] == '998') or (
                phone[:3] == '998' and len(phone) == 12) or (len(phone) == 9):
            phone_number = phone
        else:
            update.message.reply_text("Siz telefon raqamingizni xato kiritdingiz yoki o'zbek raqam kiritmadingiz\n"
                                      "Qayta kiritib ko'ring:")
            return 'state_phone'
    context.user_data['phone'] = phone_number
    update.message.reply_text(f"Sizning Ismingiz: {context.user_data['name']}\n"
                              f"Sizning telefon raqamingiz: {phone_number}\n"
                              f"Endi esa viloyatingizni kiriting?")
    return 'state_viloyat'


def command_viloyat(update: Update, context: CallbackContext):
    text = update.message.text
    update.message.reply_html(f"Sizning ism familyangiz : <b>{context.user_data['name']}</b>\n"
                              f"Sizning raqamingiz: <b>{context.user_data['phone']}</b>\n"
                              f"Siznig viloyatingiz: <b>{text}</b>\n"
                              f"Siz muaffaqiyatli ro'yxatdan o'tdingiz")
    update.message.reply_html("Buyurtmani birga joylashtiramizmi? 🤗", reply_markup=main_button())
    add_user(update.effective_user.id, context.user_data['name'], update.effective_user.first_name,
             context.user_data['phone'], text)
    return 'state_main'


def command_category(update: Update, context: CallbackContext):
    query = update.callback_query
    data = str(query.data)
    query.message.delete()
    if data.isdigit():
        context.user_data['category_id'] = data
        cat_name = get_name_bycatid(int(data))[0]
        query.message.reply_photo(open('images/img.png', 'rb'), caption=f"Bo'lim <b>{cat_name}</b>", parse_mode='HTML',
                                  reply_markup=product_button_bycat(int(data)))
        return 'state_product'


def command_product(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    query.message.delete()
    print(data)
    if data == 'back':
        query.message.reply_text("Buyurtmani birga joylashtiramizmi? 🤗", reply_markup=main_button())
        return 'state_main'
    elif data.isdigit():
        data = get_product(int(data))
        context.user_data['product_id'] = data[0]
        xabar = f"""Siz tanladingiz: {data[2]}
Narx: {data[3]} so'm
-----
Iltimos, kerakli bo’lgan miqdorni kiriting! <a href="https://cdn.delever.uz/delever/d63c47ed-ec5e-46f0-9b21-e5a51fb42373">Nechta kerakligini tanlang?</a>"""

        query.message.reply_html(xabar, reply_markup=quantity_button())
        context.user_data['soni'] = ''
        return 'state_product_quantity'


def command_product_quantity(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    if data.isdigit():
        soni = '0'
        if context.user_data['soni']:
            if context.user_data['soni'] == '0':
                context.user_data['soni'] = ''
            soni = context.user_data['soni'] + data
            context.user_data['soni'] = soni
        elif data != '0' and not (context.user_data['soni']):
            soni = data
            context.user_data['soni'] = soni
        else:
            return 'state_product_quantity'
        query.message.edit_reply_markup(reply_markup=quantity_button(soni))
    elif data == 'delete':
        if context.user_data['soni'] and context.user_data['soni'] != '0':
            soni = context.user_data['soni'][:-1]
            if not (soni):
                soni = '0'
            context.user_data['soni'] = soni

            query.message.edit_reply_markup(reply_markup=quantity_button(soni))
    elif data == 'back':
        query.message.delete()
        category_id = context.user_data['category_id']
        cat_name = get_name_bycatid(int(category_id))[0]
        query.message.reply_photo(open('images/img.png', 'rb'), caption=f"Bo'lim <b>{cat_name}</b>", parse_mode='HTML',
                                  reply_markup=product_button_bycat(int(category_id)))
        return 'state_product'
    elif data == 'savat':
        if context.user_data['soni']!='0' or context.user_data['soni'] !='':
            ord_id = get_order(update.effective_user.id)
            quantity = int(context.user_data['soni'])
            product_id = context.user_data['product_id']
            add_ord_det(ord_id, product_id, quantity)
            query.message.delete()
            query.message.reply_text("Savatchaga muaffaqiyatli joylandi", reply_markup=main_button())
            return 'state_main'



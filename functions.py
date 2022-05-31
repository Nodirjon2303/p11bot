from telegram import Update
from telegram.ext import CallbackContext
from Buttons import *
from database import *


def start(update: Update, context: CallbackContext):
    if check_user(update.effective_user.id):
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


def command_category(update:Update, context:CallbackContext):
    query = update.callback_query
    data = str(query.data)
    if data.isdigit():
        cat_name = get_name_bycatid(int(data))[0]
        query.message.reply_photo(open('images/img.png', 'rb'), caption=f"Bo'lim <b>{cat_name}</b>", parse_mode='HTML', reply_markup=product_button_bycat(int(data)))




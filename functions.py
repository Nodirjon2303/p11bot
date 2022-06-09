from telegram import Update
from telegram.ext import CallbackContext
from Buttons import *
from database import *
from geopy.geocoders import Nominatim
import time
from pprint import pprint


def start(update: Update, context: CallbackContext):
    admins = [881319779, 1306354017, 903534595, 5421001823]
    if update.effective_user.id in admins:
        update.message.reply_text("Quyidagilardan birini tanlang ", reply_markup=admin_main_button())
        return 'state_admin'

    if check_user(update.effective_user.id):
        update.message.reply_text("Assalomu alaykum", reply_markup=ReplyKeyboardRemove())
        update.message.reply_text("Buyurtmani birga joylashtiramizmi? 🤗", reply_markup=main_button())
        return 'state_main'
    update.message.reply_text("Assalomu alaykum Botimizga xush kelibsiz\n"
                              "Ro'yxatdan o'tish uchun FIO ni yuboring", reply_markup=ReplyKeyboardRemove())
    return 'state_name'

def command_admin_main(update:Update, context:CallbackContext):
    data = update.message.text
    if data == 'Kategoriya qo\'shish':
        update.message.reply_html("<b>Yangi kategoriya nomini kiriting</b>", reply_markup=ReplyKeyboardRemove())
        return 'state_add_category'
    elif 'Mahsulot qo\'shish':
        pass


def command_add_category(update:Update, context:CallbackContext):
    category = update.message.text
    add_category(category)
    update.message.reply_text("Kategoriya muaffaqiyatli qo'shildi", reply_markup=admin_main_button())
    return 'state_admin'

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
    elif data == 'savatcha':
        order_id = get_order(update.effective_user.id)
        context.user_data['order_id'] = order_id
        order_details = get_order_products(order_id)
        if len(order_details) == 0:
            query.message.reply_html("Sizning Savatchangi bo'm bo'sh\n"
                                     "Savatchangizga mahsulot qo'shing", reply_markup=main_button())
            return 'state_main'
        else:
            xabar = ""
            sanoq = 1
            Jami = 0
            for i in order_details:
                product = get_product(i[2])
                xabar += f"""{sanoq}.{product[2]}
└ {product[2]} {i[4]} x {product[3]} = {i[4] * product[3]} so'm

"""
                sanoq += 1
                Jami += i[4] * product[3]
            xabar += f"Jami: {Jami}"
            query.message.reply_html(xabar, reply_markup=savatcha_button(order_details))
            return 'state_savatcha'
    elif data == 'history':
        orders = get_done_orders(update.effective_user.id)
        if len(orders):
            sahifalar = {}
            sanoq = 1
            for i in orders:
                sahifalar[f'{sanoq}'] = i[0]
                sanoq += 1
            context.user_data['sahifasi'] = sahifalar
            order_details = get_order_products(context.user_data['sahifasi']['1'])
            xabar = f"Buyurtma: №{context.user_data['sahifasi']['1']}\n" \
                    f"Buyurtma vaqti: {orders[0][2]} \n\n"
            sanoq = 1
            jami = 0
            for i in order_details:
                product = get_product(i[2])
                xabar += f"{sanoq}.{product[2]}: {i[4]}x{i[3]} so'm  = {i[4] * i[3]} so'm\n"
                sanoq += 1
                jami += i[4] * i[3]
            xabar += f"Jami: {jami} so'm"
            query.message.reply_text(xabar, reply_markup=history_button(1, len(orders)))
            return 'state_history'
        else:
            query.message.reply_text("Siz hali mahsulot zakaz qilmagansiz", reply_markup=main_button())
            return 'state_main'

def command_history(update:Update, context:CallbackContext):
    query = update.callback_query
    data = query.data
    print(data)
    if data == 'back':
        query.message.edit_text("Buyurtmani birga joylashtiramizmi", reply_markup=main_button())
        return 'state_main'
    elif data.isdigit():
        sahifa = int(data)
        print(context.user_data['sahifasi'])
        if len(context.user_data['sahifasi']) == sahifa and len(context.user_data['sahifasi'])!=1:
            order_id = context.user_data['sahifasi']['1']
            order = get_order_history(order_id)
            order_details = get_order_products(order_id)
            xabar = f"Buyurtma: №{context.user_data['sahifasi']['1']}\n" \
                    f"Buyurtma vaqti:  {order[2]}\n\n"
            sanoq = 1
            jami = 0
            for i in order_details:
                product = get_product(i[2])
                xabar += f"{sanoq}.{product[2]}: {i[4]}x{i[3]} so'm  = {i[4] * i[3]} so'm\n"
                sanoq += 1
                jami += i[4] * i[3]
            xabar += f"Jami: {jami} so'm"
            query.message.edit_text(xabar, reply_markup=history_button(1, len(context.user_data['sahifasi'])))
            return 'state_history'
        elif sahifa<len(context.user_data['sahifasi']):
            order_id = context.user_data['sahifasi'][f"{sahifa+1}"]
            order = get_order_history(order_id)
            order_details = get_order_products(order_id)
            xabar = f"Buyurtma: №{context.user_data['sahifasi'][f'{sahifa+1}']}\n" \
                    f"Buyurtma vaqti:  {order[2]}\n\n"
            sanoq = 1
            jami = 0
            for i in order_details:
                product = get_product(i[2])
                xabar += f"{sanoq}.{product[2]}: {i[4]}x{i[3]} so'm  = {i[4] * i[3]} so'm\n"
                sanoq += 1
                jami += i[4] * i[3]
            xabar += f"Jami: {jami} so'm"
            query.message.edit_text(xabar, reply_markup=history_button(sahifa+1, len(context.user_data['sahifasi'])))
            return 'state_history'



def command_savatcha(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    if data == 'product':
        return 'state_savatcha'
    elif data == 'again':
        query.message.delete()
        query.message.reply_text("Buyurtmangizni davom ettirishingiz mumkin", reply_markup=main_button())
        return 'state_main'
    elif data == 'confirm':
        query.message.delete()
        query.message.reply_html("Yaxshi endi bizga manzilingizni yuboring", reply_markup=location_button())
        return 'state_location'
    else:
        type, id = data.split('_')
        if type == 'plus':
            update_order_detail_plus(int(id))
        elif type == 'minus':
            if check_order_detail(int(id)):
                update_order_detail_minus(int(id))

        order_id = get_order(update.effective_user.id)
        order_details = get_order_products(order_id)
        if len(order_details) == 0:
            query.message.edit_text("Sizning Savatchangi bo'm bo'sh\n"
                                    "Savatchangizga mahsulot qo'shing", reply_markup=main_button())
            return 'state_main'
        else:
            xabar = ""
            sanoq = 1
            Jami = 0
            for i in order_details:
                product = get_product(i[2])
                xabar += f"""{sanoq}.{product[2]}
└ {product[2]} {i[4]} x {product[3]} = {i[4] * product[3]} so'm
    
            """
                sanoq += 1
                Jami += i[4] * product[3]
            xabar += f"Jami: {Jami}"
            query.message.edit_text(xabar, reply_markup=savatcha_button(order_details), parse_mode='HTML')
            return 'state_savatcha'


def command_location(update: Update, context: CallbackContext):
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    app = Nominatim(user_agent="tutorial")
    coordinates = f"{latitude}, {longitude}"
    manzil = app.reverse(coordinates, language='eng').raw['display_name']
    context.user_data['latitude'] = latitude
    context.user_data['longitude'] = longitude
    context.user_data['manzil'] = manzil
    update.message.reply_text(manzil + "\n"
                                       "Sizning manzilingiz to'g'riligini tasdiqlang",
                              reply_markup=check_location_button())
    return 'state_check_location'


def command_confirm(update: Update, context: CallbackContext):
    print(context.user_data)
    update.message.reply_text("Sizning zakazingiz muaffaqiyatli qabul qilindi", reply_markup=main_button())
    change_order_status(context.user_data['order_id'])
    xabar = 'Yangi Zakaz!!!\n' \
            f"Zakaz: <b>{context.user_data['order_id']}</b>\n" \
            f"Mahsulotlar: \n"
    order_dets = get_order_products(context.user_data['order_id'])
    for i in order_dets:
        product = get_product(i[2])
        xabar += f"{product[2]} ==> {i[4]} * {product[3]} = {i[4] * product[3]} \n"
    xabar += f"{context.user_data['manzil']}"
    context.bot.send_message(-1001529417057, xabar, parse_mode="HTML")
    context.bot.send_location(-1001529417057, context.user_data['latitude'], context.user_data['longitude'])

    return 'state_main'


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
    print(context.user_data)
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
        if context.user_data['soni'] != '0' and context.user_data['soni'] != '':
            ord_id = get_order(update.effective_user.id)
            quantity = int(context.user_data['soni'])
            product_id = context.user_data['product_id']
            add_ord_det(ord_id, product_id, quantity)
            query.message.delete()
            query.message.reply_text("Savatchaga muaffaqiyatli joylandi", reply_markup=main_button())
            return 'state_main'
        else:
            context.bot.answerCallbackQuery(query.id, "Sizning tanlangan mahsulot soni 0 ta!!!", show_alert=True)

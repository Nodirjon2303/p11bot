import datetime
from sqlite3 import connect


def create_table_users():
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY UNIQUE ,
    telegram_id INTEGER , 
    full_name VARCHAR (185), 
    first_name VARCHAR (125), 
    phone VARCHAR (20),
    viloyat VARCHAR (125)
    )
    """)

    conn.commit()


# create_table_users()
def create_table_category():
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY UNIQUE, 
    name VARCHAR (125)
    )
    """)

    conn.commit()
    conn.commit()


def create_table_product():
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY UNIQUE, 
    cat_id INTEGER , 
    name VARCHAR (125), 
    price integer, 
    image VARCHAR (125) 
    )
    """)

    conn.commit()


def create_table_order():
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY UNIQUE,
    user_id INTEGER , 
    order_date datetime, 
    status Varchar(125) default 'progress'
    )
    """)

    conn.commit()


def create_table_order_detail():
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Order_detail (
    id INTEGER PRIMARY KEY UNIQUE,
    order_id INTEGER , 
    product_id INTEGER ,
    unit_price INTEGER , 
    quantity INTEGER
    )
    """)

    conn.commit()


# create_table_order_detail()

# create_table_order()

def get_all_categories():
    conn = connect('main.db')
    cursor = conn.cursor()

    cursor.execute("""
    select * from category    
    """)
    data = cursor.fetchall()
    return data


# print(get_all_categories())
def get_products_by_catid(cat_id):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT * from products
    where cat_id = {cat_id}
    """)
    data = cursor.fetchall()
    return data


def get_name_bycatid(cat_id):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT name from category
    where id = {cat_id}
    """)
    data = cursor.fetchone()
    return data


# print(get_name_bycatid(2))

def add_user(telegram_id, full_name, first_name, phone, viloyat):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    INSERT INTO users (telegram_id, full_name, first_name, phone, viloyat)
    VALUES ({telegram_id}, "{full_name}", "{first_name}", '{phone}', "{viloyat}")
    """)
    conn.commit()


def add_category(cat_name):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    INSERT INTO category (name)
    values ("{cat_name}")
    """)
    conn.commit()


def add_product(cat_id, name, price):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    INSERT INTO products (cat_id, name, price)
    values ({cat_id}, "{name}", {price})
    """)
    conn.commit()


def set_unit_price(order_det_id, price):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
        UPDATE Order_detail
        set unit_price = {price}
        where id = {order_det_id}
        """)
    conn.commit()


def add_ord_det(order_id, product_id, quant):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    select * from Order_detail
    where order_id = {order_id} and product_id = {product_id}
    """)
    data = cursor.fetchall()
    if not data:
        cursor.execute(f"""
        INSERT INTO Order_detail (order_id, product_id, quantity)
        VALUES ({order_id}, {product_id}, {quant})
        """)
        conn.commit()
    else:
        cursor.execute(f"""
        UPDATE Order_detail
        SET quantity = quantity+{quant}
        where order_id = {order_id} and product_id = {product_id}
        """)
        conn.commit()


def check_user(telegram_id):
    conn = connect('main.db')
    cursor = conn.cursor()

    cursor.execute(f"""
    select * from users
    where telegram_id = {telegram_id}
    """)
    data = cursor.fetchone()
    if data:
        return True
    else:
        return False


def get_product(product_id):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
        select * from products
        where id = {product_id}
        """)
    data = cursor.fetchone()
    return data


def get_done_orders(telegram_id):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
        select * from Orders
        where user_id = (select id from users
                         where telegram_id = {telegram_id}
        ) and status = 'done'
        order by order_id 
        """)
    data = cursor.fetchall()
    return data


def get_order_history(order_id):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
            select * from Orders
            where order_id = {order_id}
            """)
    data = cursor.fetchone()
    return data


# order = get_order_history(1)
# print(order[2])

# print(get_done_orders(881319779))


def get_order(telegram_id):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    select * from Orders
    where user_id = (select id from users
                where telegram_id = {telegram_id}
    ) and status = 'progress'
    """)
    data = cursor.fetchone()
    if not (data):
        cursor.execute(f"""
        INSERT INTO Orders (user_id)
        values
        ((select id from users
                where telegram_id = {telegram_id}))
        """)
        conn.commit()
        cursor.execute(f"""
            select * from Orders
            where user_id = (select id from users
                        where telegram_id = {telegram_id}
            ) and status = 'progress'
            """)
        data = cursor.fetchone()
        return data[0]
    else:
        return data[0]


def get_order_products(order_id):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    select * from Order_detail
    where order_id = {order_id}
    """)
    data = cursor.fetchall()

    return data


print(get_order_products(2))


def get_product(product_id):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
        select * from products
        where id = {product_id}
        """)
    data = cursor.fetchone()
    return data


def update_order_detail_plus(id):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
            UPDATE Order_detail
            SET quantity = quantity+1
            where id = {id}
            """)
    data = cursor.fetchone()
    return data


def update_order_detail_plus(id):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
            UPDATE Order_detail
            SET quantity = quantity+1
            where id = {id}
            """)
    conn.commit()


def update_order_detail_minus(id):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
            UPDATE Order_detail
            SET quantity = quantity-1
            where id = {id}
            """)
    conn.commit()


def change_order_status(order_id):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
                UPDATE Orders
                SET status = 'done', order_date = CURRENT_TIMESTAMP
                where order_id = {order_id}
                """)
    conn.commit()


def check_order_detail(id):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    select quantity from Order_detail
    where  id = {id}
    """)
    data = cursor.fetchone()[0]
    if data == 1:
        cursor.execute(f"""
            DELETE FROM Order_detail
            where id = {id}
            """)
        conn.commit()
        return False
    else:
        return True


#
# print(get_order_products(2))
# print(get_product(1))

# print(get_order(903534595))
# print(get_product(1))
print(get_product(1))

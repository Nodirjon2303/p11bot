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
print(get_name_bycatid(2))

def add_user(telegram_id, full_name, first_name, phone, viloyat):
    conn = connect('main.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    INSERT INTO users (telegram_id, full_name, first_name, phone, viloyat)
    VALUES ({telegram_id}, "{full_name}", "{first_name}", '{phone}', "{viloyat}")
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

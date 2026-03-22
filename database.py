import sqlite3

def get_db():
    conn = sqlite3.connect("soulbond.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    # productos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    # variantes (talla/color)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS variants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        color TEXT,
        size TEXT,
        price INTEGER
    )
    """)

    # pedidos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contact TEXT,
        total INTEGER
    )
    """)
def seed_products():
    conn = get_db()

    # Skull cap
    conn.execute("INSERT INTO products (name) VALUES ('Skull Cap')")

    # Short camuflados
    conn.execute("INSERT INTO products (name) VALUES ('Short Camuflados')")

    # Slim fit
    conn.execute("INSERT INTO products (name) VALUES ('Polera Slim Fit')")

    # Baby tee
    conn.execute("INSERT INTO products (name) VALUES ('Baby Tee')")

    # Poleras normales
    conn.execute("INSERT INTO products (name) VALUES ('Poleras Clasicas')")

    conn.commit()
    conn.close()
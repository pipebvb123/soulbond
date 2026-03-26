import sqlite3

def get_db():
    conn = sqlite3.connect("soulbond.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        image TEXT
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contact TEXT,
        total INTEGER
    )
    """)

    conn.commit()
    conn.close()

def seed_products():
    conn = get_db()

    count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]

    if count == 0:
        conn.execute("INSERT INTO products (name, price, image) VALUES ('Skull Cap', 9990, 'https://via.placeholder.com/300')")
        conn.execute("INSERT INTO products (name, price, image) VALUES ('Short Camuflados', 19990, 'https://via.placeholder.com/300')")
        conn.execute("INSERT INTO products (name, price, image) VALUES ('Polera Slim Fit', 14990, 'https://via.placeholder.com/300')")
        conn.execute("INSERT INTO products (name, price, image) VALUES ('Baby Tee', 12990, 'https://via.placeholder.com/300')")
        conn.execute("INSERT INTO products (name, price, image) VALUES ('Poleras Clasicas', 10990, 'https://via.placeholder.com/300')")

    conn.commit()
    conn.close()

    
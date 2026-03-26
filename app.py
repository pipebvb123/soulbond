from flask import Flask, render_template, request, redirect, session
from database import get_db, init_db, seed_products
import urllib.parse

app = Flask(__name__)
app.secret_key = "soulbond_secret"

init_db()
seed_products()

# 🔹 PRODUCTOS
def get_products():
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return products

@app.route("/")
def index():
    products = get_products()
    return render_template("index.html", products=products)

@app.route("/product/<int:id>")
def product(id):
    conn = get_db()
    product = conn.execute("SELECT * FROM products WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("product.html", product=product)

# 🛒 CARRITO
@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    cart = session.get("cart", {})

    id = str(id)

    if id in cart:
        cart[id] += 1
    else:
        cart[id] = 1

    session["cart"] = cart


    return redirect("/cart")

@app.route("/remove/<int:id>")
def remove(id):
    cart = session.get("cart", {})
    cart.pop(str(id), None)
    session["cart"] = cart
    return redirect("/cart")

@app.route("/cart")
def cart():
    cart_items = []
    total = 0

    conn = get_db()

    for id, qty in session.get("cart", {}).items():
        product = conn.execute("SELECT * FROM products WHERE id=?", (int(id),)).fetchone()

        if product:
            product = dict(product)
            
            price = product.get("price") or 0

            product["qty"] = qty
            product["subtotal"] = price * qty

            cart_items.append(product)
            total += price * qty

    conn.close()

    return render_template("cart.html", items=cart_items, total=total)

# 💳 CHECKOUT
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        contact = request.form["contact"]
        method = request.form["payment_method"]

        total = 0
        conn = get_db()

        for id, qty in session.get("cart", {}).items():
            product = conn.execute("SELECT * FROM products WHERE id=?", (int(id),)).fetchone()

            if product:
                total += (product["price"] or 0) * qty

        conn.execute("INSERT INTO orders (contact, total) VALUES (?, ?)", (contact, total))
        conn.commit()
        conn.close()

        session["cart"] = {}

        # 💳 TARJETA → redirige a pago externo (simulado)
        if method == "card":
            return render_template("success.html", total=total)

        # 🏦 TRANSFERENCIA → muestra datos + WhatsApp
        if method == "transfer":
            mensaje = urllib.parse.quote(f"Hola! hice un pedido por ${total}")
            link = f"https://wa.me/56992508009?text={mensaje}"

            return render_template("transfer.html", total=total, link=link)

    return render_template("checkout.html")

# 📦 PEDIDOS
@app.route("/orders")
def orders():
    if request.args.get("key") != "898369":
        return "No autorizado"

    conn = get_db()
    orders = conn.execute("SELECT * FROM orders").fetchall()
    conn.close()

    return render_template("orders.html", orders=orders)









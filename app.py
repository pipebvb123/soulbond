from flask import Flask, render_template, request, redirect, session
from database import get_db, init_db, seed_products
import mercadopago


app = Flask(__name__)
app.secret_key = "soulbond_secret"

init_db()
seed_products()

sdk = mercadopago.SDK("TEST-APP_USR-7609628854752746-032216-75ea60017159dcb348f58def7ebcbdd8-3284095970S")





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

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    cart = session.get("cart", {})

    id = str(id)

    if id in cart:
        cart[id] += 1
    else:
        cart[id] = 1

    session["cart"] = cart
    session.modified = True

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
        product = conn.execute(
            "SELECT * FROM products WHERE id=?", (int(id),)
        ).fetchone()

        if product:
            product = dict(product)

            price = product.get("price") or 0

            product["qty"] = qty
            product["subtotal"] = price * qty

            cart_items.append(product)
            total += price * qty

    conn.close()

    return render_template("cart.html", items=cart_items, total=total)


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        contact = request.form["contact"]

        total = 0
        conn = get_db()

        for id, qty in session.get("cart", {}).items():
            product = conn.execute(
                "SELECT * FROM products WHERE id=?", (int(id),)
            ).fetchone()

            if product:
                price = product["price"] or 0
                total += price * qty

        conn.execute(
            "INSERT INTO orders (contact, total) VALUES (?, ?)",
            (contact, total)
        )
        conn.commit()
        conn.close()

        session["cart"] = {}

        return "Compra realizada ✅ Te contactaremos"

    return render_template("checkout.html")


@app.route("/orders")
def view_orders():
    if request.args.get("key") != "898369":
        return "No autorizado"

    conn = get_db()
    orders = conn.execute("SELECT * FROM orders").fetchall()
    conn.close()

    return render_template("orders.html", orders=orders)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

from flask import Flask, render_template, request, redirect, session
import mercadopago
from database import get_db, init_db

app = Flask(__name__)
app.secret_key = "soulbond_secret"

init_db()

sdk = mercadopago.SDK("TEST-APP_USR-7609628854752746-032216-75ea60017159dcb348f58def7ebcbdd8-3284095970")

# 🔹 Obtener productos desde DB
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
    if "cart" not in session:
        session["cart"] = {}

    cart = session["cart"]

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    session["cart"] = cart
    return redirect("/")

@app.route("/cart")
def cart():
    cart_items = []
    total = 0

    conn = get_db()

    for id in session.get("cart", []):
        product = conn.execute("SELECT * FROM products WHERE id=?", (id,)).fetchone()
        if product:
            cart_items.append(product)
            total += product["price"]

    conn.close()

    return render_template("cart.html", items=cart_items, total=total)

# 🔐 ADMIN
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.args.get("key") != "898369":
        return "No autorizado"

    if request.method == "POST":
        name = request.form["name"]
        price = int(request.form["price"])
        image = request.form["image"]

        conn = get_db()
        conn.execute(
            "INSERT INTO products (name, price, image) VALUES (?, ?, ?)",
            (name, price, image)
        )
        conn.commit()
        conn.close()

    products = get_products()
    return render_template("admin.html", products=products)

# 💳 CHECKOUT
@app.route("/checkout", methods=["GET","POST"])
def checkout():
    if request.method == "POST":
        contact = request.form["contact"]

        total = 0
        conn = get_db()

        for id, qty in session.get("cart", {}).items():
            product = conn.execute("SELECT * FROM products WHERE id=?", (id,)).fetchone()
            if product:
                total += 10000 * int(qty)  # ejemplo

        conn.execute("INSERT INTO orders (contact,total) VALUES (?,?)",(contact,total))
        conn.commit()
        conn.close()

        session["cart"] = {}

        return "Compra realizada ✅ Te contactaremos"

    return render_template("checkout.html")

# 📦 VER PEDIDOS
@app.route("/orders")
def view_orders():
    if request.args.get("key") != "898369":
        return "No autorizado"

    conn = get_db()
    orders = conn.execute("SELECT * FROM orders").fetchall()
    conn.close()

    return render_template("orders.html", orders=orders)

# 🚀 RUN
if __name__ == "__main__":
    app.run(debug=True)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]

        conn = get_db()
        u = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (user,password)).fetchone()
        conn.close()

        if u:
            session["user"] = user
            return redirect("/")
    
    return render_template("login.html")    

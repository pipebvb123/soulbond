from flask import Flask, render_template, request, redirect, session
import mercadopago
sdk = mercadopago.SDK("TU_ACCESS_TOKEN")

app = Flask(__name__)
app.secret_key = "soulbond_secret"

products = [
    {"id": 1, "name": "Soulbond Hoodie Black", "price": 29990, "image": "https://via.placeholder.com/400", "rating": 5},
    {"id": 2, "name": "Soulbond Tee Purple", "price": 19990, "image": "https://via.placeholder.com/400", "rating": 4},
    {"id": 3, "name": "Soulbond Oversize Tee", "price": 24990, "image": "https://via.placeholder.com/400", "rating": 5},
    {"id": 4, "name": "Soulbond Essentials Hoodie", "price": 34990, "image": "https://via.placeholder.com/400", "rating": 4},
]

@app.route("/")
def index():
    query = request.args.get("q")

    if query:
        filtered = [p for p in products if query.lower() in p["name"].lower()]
    else:
        filtered = products

    return render_template("index.html", products=filtered)

@app.route("/product/<int:id>")
def product(id):
    product = next((p for p in products if p["id"] == id), None)
    return render_template("product.html", product=product)

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(id)
    session.modified = True

    return redirect("/")

@app.route("/cart")
def cart():
    cart_items = []
    total = 0

    for id in session.get("cart", []):
        product = next((p for p in products if p["id"] == id), None)
        if product:
            cart_items.append(product)
            total += product["price"]

    return render_template("cart.html", items=cart_items, total=total)

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/checkout")
def checkout():
    items = []

    for id in session.get("cart", []):
        product = next((p for p in products if p["id"] == id), None)
        if product:
            items.append({
                "title": product["name"],
                "quantity": 1,
                "currency_id": "CLP",
                "unit_price": product["price"]
            })

    preference_data = {
        "items": items,
    }

    preference = sdk.preference().create(preference_data)
    return redirect(preference["response"]["init_point"])  

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        name = request.form["name"]
        price = int(request.form["price"])
        image = request.form["image"]

        new_product = {
            "id": len(products) + 1,
            "name": name,
            "price": price,
            "image": image,
            "rating": 5
        }

        products.append(new_product)

    return render_template("admin.html", products=products)

@app.route("/admin")
def admin():
    password = request.args.get("key")
    if password != "898369":
        return "No autorizado"
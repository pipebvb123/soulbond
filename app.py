from flask import Flask, render_template, request, redirect, session

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
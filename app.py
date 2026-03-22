from flask import Flask, render_template

app = Flask(__name__)

products = [
    {"id": 1, "name": "Soulbond Hoodie Black", "price": 29990, "image": "https://via.placeholder.com/400"},
    {"id": 2, "name": "Soulbond Tee Purple", "price": 19990, "image": "https://via.placeholder.com/400"},
    {"id": 3, "name": "Soulbond Oversize Tee", "price": 24990, "image": "https://via.placeholder.com/400"},
    {"id": 4, "name": "Soulbond Essentials Hoodie", "price": 34990, "image": "https://via.placeholder.com/400"},
]

@app.route("/")
def index():
    return render_template("index.html", products=products)

@app.route("/product/<int:id>")
def product(id):
    product = next((p for p in products if p["id"] == id), None)
    return render_template("product.html", product=product)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from routes.inventory import inventory_bp

# ---------------- CREATE APP ----------------
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ---------------- MONGODB CONNECTION ----------------
client = MongoClient("mongodb://localhost:27017/")
db = client["inventory_db"]
products = db["products"]

# ---------------- REGISTER BLUEPRINT ----------------
app.register_blueprint(inventory_bp)

# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return jsonify({"status": "Backend running"})

# ---------------- STATS (FOR KPI & DASHBOARD) ----------------
@app.route("/stats", methods=["GET"])
def get_stats():
    all_products = list(products.find({}, {"_id": 0}))

    total_products = len(all_products)
    total_quantity = sum(p["qty"] for p in all_products)
    low_stock = len([p for p in all_products if p["qty"] < 10])
    inventory_value = sum(p["qty"] * p["price"] for p in all_products)

    return jsonify({
        "totalProducts": total_products,
        "totalQuantity": total_quantity,
        "lowStock": low_stock,
        "inventoryValue": inventory_value,
        "products": all_products   # useful for charts
    })

# ---------------- RUN SERVER (ALWAYS LAST) ----------------
if __name__ == "__main__":
    app.run(debug=True)  
from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from routes.inventory import inventory_bp

app = Flask(__name__)
CORS(app)

# ✅ MongoDB Atlas connection (from Render env variable)
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["inventory_db"]
products = db["products"]

# Register blueprint
app.register_blueprint(inventory_bp)

@app.route("/")
def home():
    return jsonify({"status": "Backend running"})

@app.route("/stats", methods=["GET"])
def get_stats():
    all_products = list(products.find({}, {"_id": 0}))

    total_products = len(all_products)
    total_quantity = sum(p.get("qty", 0) for p in all_products)
    low_stock = len([p for p in all_products if p.get("qty", 0) < 10])
    inventory_value = sum(p.get("qty", 0) * p.get("price", 0) for p in all_products)

    return jsonify({
        "totalProducts": total_products,
        "totalQuantity": total_quantity,
        "lowStock": low_stock,
        "inventoryValue": inventory_value,
        "products": all_products
    })

if __name__ == "__main__":
    app.run()

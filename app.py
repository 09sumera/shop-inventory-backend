from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# ✅ MongoDB Atlas (from Render ENV)
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["inventory_db"]
products = db["products"]

# ✅ make products available to blueprints
app.config["PRODUCTS_COLLECTION"] = products

# register routes AFTER db setup
from routes.inventory import inventory_bp
app.register_blueprint(inventory_bp)

@app.route("/")
def home():
    return jsonify({"status": "Backend running"})

@app.route("/stats")
def stats():
    all_products = list(products.find({}, {"_id": 0}))

    return jsonify({
        "totalProducts": len(all_products),
        "totalQuantity": sum(p.get("qty", 0) for p in all_products),
        "lowStock": len([p for p in all_products if p.get("qty", 0) < 10]),
        "inventoryValue": sum(p.get("qty", 0) * p.get("price", 0) for p in all_products),
        "products": all_products
    })

if __name__ == "__main__":
    app.run()
